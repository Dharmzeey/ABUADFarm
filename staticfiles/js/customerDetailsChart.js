function loadChart() {
  $.get(url, { 'searchUnit': searchUnit, 'searchItem': searchItem, 'pk': pk }, (value) => {

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
        pinchZoomX: true
      }));

      chart.get("colors").set("step", 3);


      // Add cursor
      // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
      var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
      cursor.lineY.set("visible", false);


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
        renderer: am5xy.AxisRendererY.new(root, {})
      }));


      // Create series
      // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
      var series = chart.series.push(am5xy.LineSeries.new(root, {
        name: "Series 1",
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "value",
        valueXField: "date",
        tooltip: am5.Tooltip.new(root, {
          labelText: "{valueY}"
        })
      }));
      series.strokes.template.setAll({
        strokeWidth: 2,
        strokeDasharray: [2, 0]
      });

      // Create animating bullet by adding two circles in a bullet container and
      // animating radius and opacity of one of them.
      series.bullets.push(function (root, series, dataItem) {
        if (dataItem.dataContext.bullet) {
          var container = am5.Container.new(root, {});
          var circle0 = container.children.push(am5.Circle.new(root, {
            radius: 5,
            fill: am5.color(0xff0000)
          }));
          var circle1 = container.children.push(am5.Circle.new(root, {
            radius: 5,
            fill: am5.color(0xff0000)
          }));

          circle1.animate({
            key: "radius",
            to: 20,
            duration: 1000,
            easing: am5.ease.out(am5.ease.cubic),
            loops: Infinity
          });
          circle1.animate({
            key: "opacity",
            to: 0,
            from: 1,
            duration: 1000,
            easing: am5.ease.out(am5.ease.cubic),
            loops: Infinity
          });

          return am5.Bullet.new(root, {
            sprite: container
          })
        }
      })

      // THIS CODE HERE TAKES IN THE SERIALIZED DATA FROM THE DRF AND THEN GRUOP ALL THE GOODS BASED ON DATE_ORDERED INTO DICTIONARY 
      // IT FIRST GET THE DAY, MONTH AND YEAR AND THE PASS IT INTO A DATE OBJECT AND THEN PERFORM THE.getTime() METHOD 
      let dataDict = {}
      for (let i = 0; i < value['data'].length; i++) {
        const dateOrdered = new Date(value["data"][i]["date_ordered"])
        const year = dateOrdered.getUTCFullYear()
        const month = dateOrdered.getUTCMonth()
        const date = dateOrdered.getUTCDate()
        let dayOrdered = new Date(year, month, date).getTime()
        // IT CHECKS IF THE KEY OF "DATE" ALREADY IN dataDict, IF IT DOES IT APPENDS THE GOOD TO THE ARRAY OF THE DATE ELSE IT WILL CREATE A NEW ARRAY OF DICT DATE
        if (dayOrdered in dataDict) {
          dataDict[dayOrdered] += parseFloat(value["data"][i]["price"])
        }
        // IF KEY DATE IS NOT AVAILABLE IT WILL SET THE dateValue AND CREATE A NEW LIST
        else if (!(dayOrdered in dataDict)) {
          dataDict[dayOrdered] = parseFloat(value["data"][i]["price"])
        }
      }

      // THIS GETS THE KEY VALUE OF THE DICT OF dataDict
      let entries = Object.entries(dataDict)
      // Set data
      var data = []
      for ([key, values] of entries) {
        dictData = {}
        dictData.date = parseInt(key)
        dictData.value = parseInt(values)
        data.push(dictData)
      }
      // THIS BELOW ADDS BULLET TO THE LAST ITEM
      data[0].bullet = true 
      // I HAVE TO REVERSE THE ARRAY SO PRICE CAN DISPLAY ON THE CHART
      data = data.reverse()

      series.data.setAll(data);

      // Make stuff animate on load
      // https://www.amcharts.com/docs/v5/concepts/animations/
      series.appear(1000);
      chart.appear(1000, 100);

    }); // end am5.ready()
  })
}