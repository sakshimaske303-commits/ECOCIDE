def create_world_file(image_path, bbox, width_px, height_px):
    min_lon, min_lat, max_lon, max_lat = bbox
    pixel_width = (max_lon - min_lon) / width_px
    pixel_height = -(max_lat - min_lat) / height_px

    world_file_path = image_path.rsplit(".", 1)[0] + ".pgw"
    with open(world_file_path, "w") as f:
        f.write(f"{pixel_width}\n0.0\n0.0\n{pixel_height}\n{min_lon}\n{max_lat}\n")
    print(f"Created: {world_file_path}")


BBOX = [32.0, 46.3, 33.6, 46.9]
create_world_file("data/satellite_imagery/after_july2023.png", BBOX, 1600, 1200)