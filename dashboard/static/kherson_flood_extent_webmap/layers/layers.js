var wms_layers = [];


        var lyr_GoogleHybrid_0 = new ol.layer.Tile({
            'title': 'Google Hybrid',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
            attributions: '<a href="https://www.google.at/permissions/geoguidelines/attr-guide.html">Map data ©2015 Google</a>',
                url: 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}'
            })
        });
var format_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1 = new ol.format.GeoJSON();
var features_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1 = format_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.readFeatures(json_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.addFeatures(features_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1);
var lyr_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1, 
                style: style_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1,
                popuplayertitle: 'ST1_20230621_FloodExtent_KhersonskarOblast_UKR',
                interactive: false,
                title: '<img src="styles/legend/ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.png" /> ST1_20230621_FloodExtent_KhersonskarOblast_UKR'
            });
var format_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2 = new ol.format.GeoJSON();
var features_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2 = format_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.readFeatures(json_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.addFeatures(features_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2);
var lyr_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2, 
                style: style_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2,
                popuplayertitle: 'ST3_20230606_FloodExtent_KhersonskaOblast_UKR',
                interactive: false,
                title: '<img src="styles/legend/ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.png" /> ST3_20230606_FloodExtent_KhersonskaOblast_UKR'
            });
var format_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3 = new ol.format.GeoJSON();
var features_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3 = format_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.readFeatures(json_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.addFeatures(features_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3);
var lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3 = new ol.layer.Vector({
                declutter: false,
                source:jsonSource_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3, 
                style: style_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3,
                popuplayertitle: 'ST3_20230609_FloodExtent_KhersonskaOblast_UKR',
                interactive: false,
                title: '<img src="styles/legend/ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.png" /> ST3_20230609_FloodExtent_KhersonskaOblast_UKR'
            });

lyr_GoogleHybrid_0.setVisible(true);lyr_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.setVisible(true);lyr_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.setVisible(true);lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.setVisible(true);
var layersList = [lyr_GoogleHybrid_0,lyr_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1,lyr_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2,lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3];
lyr_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.set('fieldAliases', {'Water_Cl_1': 'Water_Cl_1', 'Sensor_D_1': 'Sensor_D_1', 'Confiden_1': 'Confiden_1', 'Field_Va_1': 'Field_Va_1', 'Water_St_1': 'Water_St_1', 'SenorID__1': 'SenorID__1', 'SHAPE_Leng': 'SHAPE_Leng', 'SHAPE_Area': 'SHAPE_Area', 'Water_Clas': 'Water_Clas', 'Sensor_ID': 'Sensor_ID', 'Sensor_Dat': 'Sensor_Dat', 'Confidence': 'Confidence', 'Field_Vali': 'Field_Vali', 'Water_Stat': 'Water_Stat', 'Notes': 'Notes', 'Area_m2': 'Area_m2', 'Area_ha': 'Area_ha', 'SenorID_ol': 'SenorID_ol', 'StaffID': 'StaffID', 'EventCode': 'EventCode', });
lyr_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.set('fieldAliases', {'SHAPE_Leng': 'SHAPE_Leng', 'SHAPE_Area': 'SHAPE_Area', 'Water_Clas': 'Water_Clas', 'Sensor_ID': 'Sensor_ID', 'Sensor_Dat': 'Sensor_Dat', 'Confidence': 'Confidence', 'Field_Vali': 'Field_Vali', 'Water_Stat': 'Water_Stat', 'Notes': 'Notes', 'Area_m2': 'Area_m2', 'Area_ha': 'Area_ha', 'SenorID_ol': 'SenorID_ol', 'StaffID': 'StaffID', 'EventCode': 'EventCode', });
lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.set('fieldAliases', {'Water_Clas': 'Water_Clas', 'Sensor_ID': 'Sensor_ID', 'Sensor_Dat': 'Sensor_Dat', 'Confidence': 'Confidence', 'Field_Vali': 'Field_Vali', 'Water_Stat': 'Water_Stat', 'Notes': 'Notes', 'Area_m2': 'Area_m2', 'Area_ha': 'Area_ha', 'SenorID_ol': 'SenorID_ol', 'StaffID': 'StaffID', 'EventCode': 'EventCode', 'SHAPE_Leng': 'SHAPE_Leng', 'SHAPE_Area': 'SHAPE_Area', });
lyr_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.set('fieldImages', {'Water_Cl_1': 'TextEdit', 'Sensor_D_1': 'DateTime', 'Confiden_1': 'TextEdit', 'Field_Va_1': 'TextEdit', 'Water_St_1': 'TextEdit', 'SenorID__1': 'TextEdit', 'SHAPE_Leng': 'TextEdit', 'SHAPE_Area': 'TextEdit', 'Water_Clas': 'TextEdit', 'Sensor_ID': 'TextEdit', 'Sensor_Dat': 'DateTime', 'Confidence': 'TextEdit', 'Field_Vali': 'TextEdit', 'Water_Stat': 'TextEdit', 'Notes': 'TextEdit', 'Area_m2': 'TextEdit', 'Area_ha': 'TextEdit', 'SenorID_ol': 'TextEdit', 'StaffID': 'TextEdit', 'EventCode': 'TextEdit', });
lyr_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.set('fieldImages', {'SHAPE_Leng': 'TextEdit', 'SHAPE_Area': 'TextEdit', 'Water_Clas': 'TextEdit', 'Sensor_ID': 'TextEdit', 'Sensor_Dat': 'DateTime', 'Confidence': 'TextEdit', 'Field_Vali': 'TextEdit', 'Water_Stat': 'TextEdit', 'Notes': 'TextEdit', 'Area_m2': 'TextEdit', 'Area_ha': 'TextEdit', 'SenorID_ol': 'TextEdit', 'StaffID': 'TextEdit', 'EventCode': 'TextEdit', });
lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.set('fieldImages', {'Water_Clas': 'Range', 'Sensor_ID': 'TextEdit', 'Sensor_Dat': 'DateTime', 'Confidence': 'Range', 'Field_Vali': 'Range', 'Water_Stat': 'TextEdit', 'Notes': 'TextEdit', 'Area_m2': 'TextEdit', 'Area_ha': 'TextEdit', 'SenorID_ol': 'Range', 'StaffID': 'TextEdit', 'EventCode': 'TextEdit', 'SHAPE_Leng': 'TextEdit', 'SHAPE_Area': 'TextEdit', });
lyr_ST1_20230621_FloodExtent_KhersonskarOblast_UKR_1.set('fieldLabels', {'Water_Cl_1': 'no label', 'Sensor_D_1': 'no label', 'Confiden_1': 'no label', 'Field_Va_1': 'no label', 'Water_St_1': 'no label', 'SenorID__1': 'no label', 'SHAPE_Leng': 'no label', 'SHAPE_Area': 'no label', 'Water_Clas': 'no label', 'Sensor_ID': 'no label', 'Sensor_Dat': 'no label', 'Confidence': 'no label', 'Field_Vali': 'no label', 'Water_Stat': 'no label', 'Notes': 'no label', 'Area_m2': 'no label', 'Area_ha': 'no label', 'SenorID_ol': 'no label', 'StaffID': 'no label', 'EventCode': 'no label', });
lyr_ST3_20230606_FloodExtent_KhersonskaOblast_UKR_2.set('fieldLabels', {'SHAPE_Leng': 'no label', 'SHAPE_Area': 'no label', 'Water_Clas': 'no label', 'Sensor_ID': 'no label', 'Sensor_Dat': 'no label', 'Confidence': 'no label', 'Field_Vali': 'no label', 'Water_Stat': 'no label', 'Notes': 'no label', 'Area_m2': 'no label', 'Area_ha': 'no label', 'SenorID_ol': 'no label', 'StaffID': 'no label', 'EventCode': 'no label', });
lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.set('fieldLabels', {'Water_Clas': 'no label', 'Sensor_ID': 'no label', 'Sensor_Dat': 'no label', 'Confidence': 'no label', 'Field_Vali': 'no label', 'Water_Stat': 'no label', 'Notes': 'no label', 'Area_m2': 'no label', 'Area_ha': 'no label', 'SenorID_ol': 'no label', 'StaffID': 'no label', 'EventCode': 'no label', 'SHAPE_Leng': 'no label', 'SHAPE_Area': 'no label', });
lyr_ST3_20230609_FloodExtent_KhersonskaOblast_UKR_3.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});