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

$('#edit-item-button').on('click', function() { // show/hide line item edit buttons
  $(".hidden-title").removeClass("hidden");
  $(".edit-hidden-btn").removeClass("hidden");
  $(".delete-hidden-btn").addClass("hidden");
  $(".style-hidden-btn").addClass("hidden");
   $(".hidden-btn").removeClass("hidden");
});

$('#delete-item-button').on('click', function() { // show/hide line item edit buttons
  $(".hidden-title").removeClass("hidden");
  $(".edit-hidden-btn").addClass("hidden");
  $(".delete-hidden-btn").removeClass("hidden");
  $(".style-hidden-btn").addClass("hidden");
  $(".hidden-btn").removeClass("hidden");
});

$('#style-item-button').on('click', function() { // show/hide line item edit buttons
  $(".hidden-title").addClass("hidden");
  $(".edit-hidden-btn").addClass("hidden");
  $(".delete-hidden-btn").addClass("hidden");
  $(".style-hidden-btn").removeClass("hidden");
  $(".hidden-btn").removeClass("hidden");
});

$('#divider-button').on('click', function() { // add/remove divider field in line item form
   $(".divider-field").toggle();
   $(".hidden-btn").toggle();
});

$('#style-button').on('click', function() { // show/hide style section in line item form
   $(".style-section").toggle();
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

$('#id_side').on('change', function() { // render shutter model image
  var prod_type = $('#id_shutter_type').val()
  var side = $(this).val()
  var model = "/static/img/model" + prod_type + "_" + side + ".png";
  $(".product-img-section").removeClass("hidden");
  $('.product-img').prop('src', model);

  if (side == "L") {
    $(".left-field").removeClass("hidden");
    $(".right-field").addClass("hidden");
  } else {
    $(".left-field").addClass("hidden");
    $(".right-field").removeClass("hidden");
  }

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
    $(".panel-field").addClass("hidden");
    $(".t-post-field").addClass("hidden");
    $("#id_t_post").val("");
    $(".side-field").removeClass("hidden");
  } else {
    $(".panel-field").removeClass("hidden");
    $(".t-post-field").removeClass("hidden");
    $(".side-field").addClass("hidden");
    $("#id_side").val("");
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
