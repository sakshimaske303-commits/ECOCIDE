import json
import pandas as pd
import statsmodels.formula.api as smf

TREATMENT_DATE = "2023-06-01"
NARROWED_PRE_START = "2023-01-01"
FAKE_DATE_BROAD = "2022-06-01"
FAKE_DATE_NARROWED = "2023-03-01"
CONTROL_ZONES = ["tulcea", "galati", "constanta", "braila"]


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment, "zone": zone_name})
    return pd.DataFrame(rows)


def ci95(model, term):
    lo, hi = model.conf_int().loc[term]
    return (round(float(lo), 4), round(float(hi), 4))


def fit_broad(df, hac=True):
    kwargs = dict(cov_type="HAC", cov_kwds={"maxlags": 3}) if hac else {}
    return smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(**kwargs)


def main():
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)
    results = {}

    # --- Main DiD (broad baseline) ---
    df = pd.concat([kherson, tulcea], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["post"] = (df["date"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)
    m_classic = fit_broad(df, hac=False)
    m_hac = fit_broad(df, hac=True)
    results["main_did"] = {
        "label": "Main DiD\n(broad baseline)",
        "coef": round(float(m_hac.params["did_term"]), 4),
        "classic_ci": ci95(m_classic, "did_term"),
        "hac_ci": ci95(m_hac, "did_term"),
        "classic_p": round(float(m_classic.pvalues["did_term"]), 4),
        "hac_p": round(float(m_hac.pvalues["did_term"]), 4),
    }

    # --- Narrowed-baseline DiD ---
    df_n = pd.concat([kherson, tulcea], ignore_index=True)
    df_n["date"] = pd.to_datetime(df_n["date"])
    df_n = df_n[df_n["date"] >= NARROWED_PRE_START]
    df_n["post"] = (df_n["date"] >= TREATMENT_DATE).astype(int)
    df_n["did_term"] = df_n["treatment"] * df_n["post"]
    df_n["month"] = df_n["date"].dt.month.astype(str)
    n_classic = fit_broad(df_n, hac=False)
    n_hac = fit_broad(df_n, hac=True)
    results["narrowed_did"] = {
        "label": "Narrowed-baseline DiD",
        "coef": round(float(n_hac.params["did_term"]), 4),
        "classic_ci": ci95(n_classic, "did_term"),
        "hac_ci": ci95(n_hac, "did_term"),
        "classic_p": round(float(n_classic.pvalues["did_term"]), 4),
        "hac_p": round(float(n_hac.pvalues["did_term"]), 4),
    }

    # --- Placebo (broad baseline) ---
    df_p = pd.concat([kherson, tulcea], ignore_index=True)
    df_p["date"] = pd.to_datetime(df_p["date"])
    df_p = df_p[df_p["date"] < "2023-06-01"]
    df_p["post"] = (df_p["date"] >= FAKE_DATE_BROAD).astype(int)
    df_p["did_term"] = df_p["treatment"] * df_p["post"]
    df_p["month"] = df_p["date"].dt.month.astype(str)
    p_classic = fit_broad(df_p, hac=False)
    p_hac = fit_broad(df_p, hac=True)
    results["placebo_broad"] = {
        "label": "Placebo\n(broad baseline)",
        "coef": round(float(p_hac.params["did_term"]), 4),
        "classic_ci": ci95(p_classic, "did_term"),
        "hac_ci": ci95(p_hac, "did_term"),
        "classic_p": round(float(p_classic.pvalues["did_term"]), 4),
        "hac_p": round(float(p_hac.pvalues["did_term"]), 4),
    }

    # --- Placebo (narrowed baseline) ---
    df_pn = pd.concat([kherson, tulcea], ignore_index=True)
    df_pn["date"] = pd.to_datetime(df_pn["date"])
    df_pn = df_pn[(df_pn["date"] >= "2023-01-01") & (df_pn["date"] < "2023-06-01")]
    df_pn["post"] = (df_pn["date"] >= FAKE_DATE_NARROWED).astype(int)
    df_pn["did_term"] = df_pn["treatment"] * df_pn["post"]
    pn_classic = smf.ols("ndvi ~ treatment + post + did_term", data=df_pn).fit()
    pn_hac = smf.ols("ndvi ~ treatment + post + did_term", data=df_pn).fit(
        cov_type="HAC", cov_kwds={"maxlags": 1}
    )
    results["placebo_narrowed"] = {
        "label": "Placebo\n(narrowed baseline)",
        "coef": round(float(pn_hac.params["did_term"]), 4),
        "classic_ci": ci95(pn_classic, "did_term"),
        "hac_ci": ci95(pn_hac, "did_term"),
        "classic_p": round(float(pn_classic.pvalues["did_term"]), 4),
        "hac_p": round(float(pn_hac.pvalues["did_term"]), 4),
    }

    # --- Multi-control panel (pooled HAC + per-zone) ---
    controls = pd.concat([load_ndvi(z, is_treatment=0) for z in CONTROL_ZONES], ignore_index=True)
    df_mc = pd.concat([kherson, controls], ignore_index=True)
    df_mc["date"] = pd.to_datetime(df_mc["date"])
    df_mc["post"] = (df_mc["date"] >= TREATMENT_DATE).astype(int)
    df_mc["did_term"] = df_mc["treatment"] * df_mc["post"]
    df_mc["month"] = df_mc["date"].dt.month.astype(str)
    mc_hac = fit_broad(df_mc, hac=True)

    per_zone = {}
    zone_labels = {
        "tulcea": "Kherson vs. Tulcea\n(primary specification)",
        "galati": "Kherson vs. Galați",
        "braila": "Kherson vs. Brăila",
        "constanta": "Kherson vs. Constanța",
    }
    for zone in CONTROL_ZONES:
        pair = df_mc[df_mc["zone"].isin(["kherson", zone])]
        m = fit_broad(pair, hac=True)
        coef = round(float(m.params["did_term"]), 4)
        pval = round(float(m.pvalues["did_term"]), 4)
        per_zone[zone] = {
            "label": zone_labels[zone],
            "coef": coef,
            "ci": ci95(m, "did_term"),
            "p": pval,
            "null": pval > 0.05,
        }

    results["multi_control_rows"] = [
        per_zone["tulcea"],
        per_zone["galati"],
        per_zone["braila"],
        per_zone["constanta"],
        {
            "label": "Pooled: all 4 controls\n(HAC)",
            "coef": round(float(mc_hac.params["did_term"]), 4),
            "ci": ci95(mc_hac, "did_term"),
            "p": round(float(mc_hac.pvalues["did_term"]), 4),
            "null": False,
            "pooled": True,
        },
    ]

    with open("outputs/model_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved: outputs/model_results.json")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
