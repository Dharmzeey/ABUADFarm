function loadChart() {
  $.get(url, { 'goodName': goodName, 'goodUnit': goodUnit }, (value) => {
    
    // AMCHARTS
    am5.ready(function () {

      // Create root element
      // https://www.amcharts.com/docs/v5/getting-started/#Root_element
      var root = am5.Root.new("chartdiv");


      // Set themes
      // https://www.amcharts.com/docs/v5/concepts/themes/
      root.setThemes([
        am5themes_Animated.new(root)
      ]);


      // Create chart
      // https://www.amcharts.com/docs/v5/charts/xy-chart/
      var chart = root.container.children.push(am5xy.XYChart.new(root, {
        panX: true,
        panY: true,
        wheelX: "panX",
        wheelY: "zoomX",
        layout: root.verticalLayout,
        pinchZoomX: true
      }));

      chart.get("colors").set("step", 3);

      // Data

      // THIS CODE HERE TAKES IN THE SERIALIZED DATA FROM THE DRF AND THEN GRUOP ALL THE GOODS BASED ON DATE_ORDERED INTO DICTIONARY 
      // IT FIRST GET THE DAY, MONTH AND YEAR AND THE PASS IT INTO A DATE OBJECT AND THEN PERFORM THE.getTime() METHOD 
      let dataDict = {}
      for (let i = 0; i < value['data'].length; i++){
        const dateOrdered = new Date(value["data"][i]["date_ordered"])
        const year = dateOrdered.getUTCFullYear()
        const month = dateOrdered.getUTCMonth()
        const date = dateOrdered.getUTCDate()
        let dayOrdered = new Date(year, month, date).getTime()
        // IT CHECKS IF THE KEY OF "DATE" ALREADY IN dataDict, IF IT DOES IT APPENDS THE GOOD TO THE ARRAY OF THE DATE ELSE IT WILL CREATE A NEW ARRAY OF DICT DATE
        if (dayOrdered in dataDict){
          dataDict[dayOrdered].push(value["data"][i])
        }
        // IF KEY DATE IS NOT AVAILABLE IT WILL SET THE dateValue AND CREATE A NEW LIST
        else if (!(dayOrdered in dataDict)){
          dataDict[dayOrdered] = [value["data"][i]] // THE FIRST SQUARE BRACKET MEANS A LIST
        }

      }

      // THIS GETS THE KEY VALUE OF THE DICT OF dataDict
      let entries = Object.entries(dataDict)

      var data=[]
      dictData = {}

      for ([key, values] of entries){
        dictData["date"] = parseInt(key)
        for (item of values){
          itemName = item["item"]["name"].toLowerCase()
          itemPrice = item["price"]
          itemPrice = Math.ceil(itemPrice)
          dictData[itemName] = itemPrice
        }
        data.push(dictData)
        // AFTER THE DICT HAS BEEN PUSHED TO DATA, IT GETS DEFAULTED TO EMPTY DICT
        dictData = {}
      }

      // Add cursor
      // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
      var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
      cursor.lineY.set("visible", true);

      // Create axes
      // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
      var xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
        maxDeviation: 0.3,
        baseInterval: {
          timeUnit: "day",
          count: 1
        },
        renderer: am5xy.AxisRendererX.new(root, {}),
        tooltip: am5.Tooltip.new(root, {})
      }));

      var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
        maxDeviation: 0.3,
        renderer: am5xy.AxisRendererY.new(root, {}),
        tooltip: am5.Tooltip.new(root, {})
      }));


      // Add series
      // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
      function createSeries(field, name, color, dashed) {
        var series = chart.series.push(am5xy.SmoothedXLineSeries.new(root, {
          name: name,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: field,
          valueXField: "date",
          stroke: color,
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "horizontal",
            getFillFromSprite: false,
            labelText: "[bold]{name}[/]\n{valueX}: [bold]{valueY}[/]"
          })
        }));

        series.get("tooltip").get("background").setAll({
          fillOpacity: 0.7,
          fill: color,
          pointerBaseWidth: 0
        });

        series.strokes.template.setAll({
          strokeWidth: 2
        });

        if (dashed) {
          series.strokes.template.set("strokeDasharray", [5, 3]);
        }

        series.data.setAll(data);
        series.appear(1000);

        return series;
      }

      // console.log(value)
      itemNameList = []
      for (let i = 0; i < value['data'].length; i++){
        let itemName = value['data'][i]['item']['name']
        if (!(itemNameList.includes(itemName))){
          itemNameList.push(itemName)
        }
      }

      for (item of itemNameList){
        // I USED THIS COMMENTED LINE TO GENERATE RANDOM HEX COLOR
        // n = "0x" + (Math.random() * 0xfffff * 1000000).toString(16).slice(0, 6)
        // console.log(n)

        // I PREDEFINED 20 COLORS THAT THE CODE WILL SELECT RANDOMLY TO DISPLAY THE CHART ON USER DASHBOARD
        colorList = [am5.color(0x60c917), am5.color(0x9ac92f), am5.color(0xe4293d), am5.color(0x350705), am5.color(0x4b904e), am5.color(0xcce606), am5.color(0x656946), am5.color(0xeb5f12), am5.color(0xa7d76a), am5.color(0xb6721e), am5.color(0xe790e0), am5.color(0xd2e273), am5.color(0xc6effd), am5.color(0x5943d6), am5.color(0xb0e5e1), am5.color(0x718f07), am5.color(0xeec8de), am5.color(0x21583c), am5.color(0x501208), am5.color(0x9b6693)]

        randomColor = colorList[Math.floor(Math.random()*colorList.length)]
        lowercaseitem = item.toLowerCase()

        // THIS IF-ELSE CHECKS IF THE PRODUCT IS SINGLE AND IF YES, IT MAKES THE LINE SOLID INSTEAD OF DASHED
        if (itemNameList.length == 1){
          createSeries(lowercaseitem, item, randomColor, false)
        }else{
          createSeries(lowercaseitem, item, randomColor, true)
        }
      }

      // Set date fields
      // https://www.amcharts.com/docs/v5/concepts/data/#Parsing_dates
      root.dateFormatter.setAll({
        dateFormat: "yyyy-MM-dd",
        dateFields: ["valueX"]
      });


      // Add legend
      // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
      var legend = chart.children.push(
        am5.Legend.new(root, {
          centerX: am5.p50,
          x: am5.p50
        })
      );

      legend.data.setAll(chart.series.values);


      // Make stuff animate on load
      // https://www.amcharts.com/docs/v5/concepts/animations/
      chart.appear(1000, 100);

    }); // end am5.ready()


  })
}

