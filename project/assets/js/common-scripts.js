$(function() {

// EVENTS
$('#id_mount').on('change', function() { // show frame field when mount = 'outside'
  var selectedItem = $(this).val();

  if (selectedItem == "Out") {
    $(".frame-field").removeClass("hidden");
  } else {
    $(".frame-field").addClass("hidden");
    $("#id_frame").val(0);
    $("#id_trim_style").val("");
  }
});

$('#id_finish').on('change', function() { // show stain field when finish = 'stain'
  var selectedItem = $(this).val();

  if (selectedItem == "Stain") {
    $(".stain-field").removeClass("hidden");
  } else {
    $(".stain-field").addClass("hidden");
    $("#id_stain").val("");
  }
});

$('#edit-items-toggle').on('click', function() { // show/hide line item edit buttons
   $(".hidden-btn").toggle();
});

$('#divider-button').on('click', function() { // add/remove divider field in line item form
   $(".divider-field").toggle();
});

$('#id_shutter_type').on('change', function() { // hide/unhide panel, center, left, and right height fields
  var selectedItem = $(this).val();

  showMeasureField(selectedItem);
});


$('#id_shutter_type').on('change', function() { // render shutter model image
  var model = "/static/img/model" + $(this).val() + ".png";
  $(".product-img-section").removeClass("hidden");
  $('.product-img').prop('src', model);
});

$('#id_payment_method').on('change', function() { // hide/unhide panel, center, left, and right height fields
  var selectedItem = $(this).val();

  if (selectedItem == 3) { // show/hide credit card fee
    $(".check-field").addClass("hidden");
    $(".cc-fee-field").removeClass("hidden");
  } else if (selectedItem == 2) {
    $(".cc-fee-field").addClass("hidden");
    $(".check-field").removeClass("hidden");
  } else {
    $(".cc-fee-field").addClass("hidden");
    $(".check-field").addClass("hidden");
  }

});


// FUNCTIONS
function showMeasureField(val){ // function to render hidden fields in line item form
  var val = val;

  if (val == 6 || val == 8 || val == 13 || val == 15) { // remove t-post from these models
    $(".t-post-field").addClass("hidden");
    $("#id_t_post").val("");
  } else {
    $(".t-post-field").removeClass("hidden");
  }

  if (val > 13) { // add panel height to model #14 and #15
    $(".panel-height-field").removeClass("hidden");
  } else {
    $(".panel-height-field").addClass("hidden");
  }

  if (val > 11) { // add left and right height to models #12 - #15
    $(".lr-height-field").removeClass("hidden");
  } else {
    $(".lr-height-field").addClass("hidden");
  }

  if (val == 13 || val == 15) { // add center height to models #13 and #15
    $(".center-height-field").removeClass("hidden");
  } else {
    $(".center-height-field").addClass("hidden");
  }

};


}); // Document is ready
