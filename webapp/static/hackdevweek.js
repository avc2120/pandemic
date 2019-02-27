 function readTextFile(file) {
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false);
  rawFile.onreadystatechange = function() {
    if (rawFile.readyState === 4) {
      if (rawFile.status === 200 || rawFile.status == 0) {
        var heatmapData = []
        var hospitals = rawFile.responseText.split("\n");
        hospitals.forEach(function(hospital) {
          var metadata = hospital.split(",")
          var hospital_name = metadata[0]
          var latitude = parseFloat(metadata[1])
          var longitude = parseFloat(metadata[2])
          var marker = new google.maps.Marker({
            position: {lat: latitude, lng: longitude},
            map: map,
            title: hospital_name,
          });
          buildHeatMap(latitude, longitude, marker, heatmapData);
          showTopVirus(latitude, longitude, hospital_name, marker, 3);
        });
      }
    }
  }
  rawFile.send(null);
}

function buildHeatMap(latitude, longitude, marker, heatmapData) {
  heatmapData.push({
    location: new google.maps.LatLng(latitude, longitude),
    weight: Math.random() * 5
  });
  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData
  });
  heatmap.set('radius', Math.random() * 100);
  heatmap.set('opacity', 0.1);
  heatmap.setMap(map);

}

function showTopVirus(latitude, longitude, hospital_name, marker, count) {
  $.getJSON("http://localhost:5000/get_top_reports?latitude=" + latitude + "&longitude=" + longitude,
    function(data) {

      var contentString = '<b>' + hospital_name + '</b><ul class=\"list-group virus-list\">';
      for (i = 0; i < count; i++) {
        contentString += '<li class=\"list-group-item d-flex justify-content-between align-items-center\">';
        contentString += data[i]['disease']
        contentString += '<span class=\"badge badge-primary badge-pill\">'
        contentString += data[i]['count'];
        contentString += '</span> </li>';
      }
      contentString += '</li></ul>';

      var infowindow = new google.maps.InfoWindow({
        content: contentString
      });

      marker.addListener('click', function() {
        infowindow.open(map, marker);
      });
    });
}

$(document).ready(function(e) {
  var count = 0;
  $("#hack-next").click(function() {
    if (count == 0) {
      $(".modal-body-1").hide();
      $(".modal-body-2").show();
      var toCdc = $('#customSwitch1').is(":checked");
      iframe = document.getElementById('modal-body-2');
      iframe.src = "/template_1?tocdc=" + toCdc
      if (toCdc) {
        $("#modal-close-button").show();
        $("#hack-next").hide();
      }
    }
    if (count == 1) {
      $(".modal-body-2").hide();
      iframe = document.getElementById('modal-body-3');
      iframe.src = "/template_2"
      $(".modal-body-3").show();
      $("#modal-close-button").show();
      $("#hack-next").hide();
    }
    count++;
  });

  function showVirusAlert() {
    $(".virus-alert").show();
    $(".modal-body-1").show();
    $(".modal-body-1").find('form')[0].reset();
    $(".modal-body-2").hide();
    $(".modal-body-3").hide();
    $("#hack-next").show();
    $("#modal-close-button").hide();
    count = 0;
  }

  $("#modal-close-button").click(function() {
    showVirusAlert();
  });

  $('#myModal').on('hidden.bs.modal', function (e) {
    showVirusAlert();
  });

  $(function () {
    $('#datepicker').datepicker();
  });
});
