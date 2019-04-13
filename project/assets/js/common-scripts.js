$(function() {

// EVENTS
$('#delete-deal-toggle').on('click', function() { // show/hide deal edit button
  $(".hidden-deal-btn").toggleClass("hidden");
  $(".goto-deal-btn").toggleClass("hidden");
});

$('#id_mount').on('change', function() { // show frame field when mount = 'outside'
  var selectedItem = $(this).val();

  if (selectedItem == "Out") {
    $(".frame-field").removeClass("hidden");
    $(".trim-field").removeClass("hidden");
  } else {
    $(".frame-field").addClass("hidden");
    $(".trim-field").addClass("hidden");
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
  $(".edit-hidden-btn").toggleClass("hidden");
  $(".delete-hidden-btn").addClass("hidden");
  $(".style-hidden-btn").addClass("hidden");
});

$('#delete-item-button').on('click', function() { // show/hide line item edit buttons
  $(".delete-hidden-btn").toggleClass("hidden");
  $(".edit-hidden-btn").addClass("hidden");
  $(".style-hidden-btn").addClass("hidden");
});

$('#status-item-button').on('click', function() { // show/hide line item edit buttons
  $(".status-hidden-btn").toggleClass("hidden");
  $(".status-colname").toggleClass("hidden");
  $(".status-dropdown").toggleClass("hidden");
});

$('#blinds-status-item-button').on('click', function() { // show/hide line item edit buttons
  $(".blinds-status-hidden-btn").toggleClass("hidden");
  $(".blinds-status-colname").toggleClass("hidden");
  $(".blinds-status-dropdown").toggleClass("hidden");
});

$('#shades-status-item-button').on('click', function() { // show/hide line item edit buttons
  $(".shades-status-hidden-btn").toggleClass("hidden");
  $(".shades-status-colname").toggleClass("hidden");
  $(".shades-status-dropdown").toggleClass("hidden");
});

$('#sunscreens-status-item-button').on('click', function() { // show/hide line item edit buttons
  $(".sunscreens-status-hidden-btn").toggleClass("hidden");
  $(".sunscreens-status-colname").toggleClass("hidden");
  $(".sunscreens-status-dropdown").toggleClass("hidden");
});

$('#style-item-button').on('click', function() { // show/hide line item edit buttons
  $(".style-hidden-btn").toggleClass("hidden");
  $(".style-colname").toggleClass("hidden");
  $(".style-dropdown").toggleClass("hidden");
  $(".edit-hidden-btn").addClass("hidden");
  $(".delete-hidden-btn").addClass("hidden");

});

$('#blinds-style-item-button').on('click', function() { // show/hide line item edit buttons
  $(".blinds-style-hidden-btn").toggleClass("hidden");
  $(".blinds-style-colname").toggleClass("hidden");
  $(".blinds-style-dropdown").toggleClass("hidden");
});

$('#shades-style-item-button').on('click', function() { // show/hide line item edit buttons
  $(".shades-style-hidden-btn").toggleClass("hidden");
  $(".shades-style-colname").toggleClass("hidden");
  $(".shades-style-dropdown").toggleClass("hidden");
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
  if (side) {
    var model = "/static/img/model" + prod_type + "_" + side + ".png";
  } else {
    var model = "/static/img/model" + prod_type + ".png";
  }

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

$('input:checkbox').on('click', function() {
  $(this).parent().parent().toggleClass("checked-row");
});

$("#checkAll").on('click', function () {
    $(".item-checkbox").prop('checked', $(this).prop('checked'));

    if ($('#checkAll:checked').length) {
        $('.nav-link').removeClass('disabled');
        $('input:submit').prop('disabled', false)
        $('.item-checkbox').parent().parent().addClass("checked-row");
    } else {
        $('.nav-link').addClass('disabled');
        $('input:submit').prop('disabled', true)
        $('.item-checkbox').parent().parent().removeClass("checked-row");
    }
});

$(".item-checkbox").on('change', function() {
  if (!$(this).prop("checked")) {
    $("#checkAll").prop("checked", false);
  }
});

$('input:checkbox').on('change', function() {
    if ($('input:checkbox:checked').length) {
        $('.nav-link').removeClass('disabled');
        $('input:submit').prop('disabled', false)
    } else {
        $('.nav-link').addClass('disabled');
        $('input:submit').prop('disabled', true)
    }
});

// Other Products
$('#id_sunscreen_type').on('change', function() { // render shutter model image
  var model = "/static/img/grid" + $(this).val() + ".png";
  $(".product-img-section").removeClass("hidden");
  $('.product-img').prop('src', model);
});

$('#id_blind_type').on('change', function() { // show stain field when finish = 'stain'
  var selectedItem = $(this).val();

  if (selectedItem == 2) {
    $(".faux-wood-field").removeClass("hidden");
  } else {
    $(".faux-wood-field").addClass("hidden");
    $("#id_faux_wood_style").val("");
  }
});


$("#checkAllBlinds").on('click', function () {
    $(".blinds-item-checkbox").prop('checked', $(this).prop('checked'));

    if ($('#checkAllBlinds:checked').length) {
        $('.nav-link').removeClass('disabled');
        $('input:submit').prop('disabled', false)
        $('.blinds-item-checkbox').parent().parent().addClass("checked-row");
    } else {
        $('.nav-link').addClass('disabled');
        $('input:submit').prop('disabled', true)
        $('.blinds-item-checkbox').parent().parent().removeClass("checked-row");
    }
});

$(".blinds-item-checkbox").on('change', function() {
  if (!$(this).prop("checked")) {
    $("#checkAllBlinds").prop("checked", false);
  }
});


$("#checkAllShades").on('click', function () {
    $(".shades-item-checkbox").prop('checked', $(this).prop('checked'));

    if ($('#checkAllShades:checked').length) {
        $('.nav-link').removeClass('disabled');
        $('input:submit').prop('disabled', false)
        $('.shades-item-checkbox').parent().parent().addClass("checked-row");
    } else {
        $('.nav-link').addClass('disabled');
        $('input:submit').prop('disabled', true)
        $('.shades-item-checkbox').parent().parent().removeClass("checked-row");
    }
});

$(".shades-item-checkbox").on('change', function() {
  if (!$(this).prop("checked")) {
    $("#checkAllShades").prop("checked", false);
  }
});


$("#checkAllSunscreens").on('click', function () {
    $(".sunscreens-item-checkbox").prop('checked', $(this).prop('checked'));

    if ($('#checkAllSunscreens:checked').length) {
        $('.nav-link').removeClass('disabled');
        $('input:submit').prop('disabled', false)
        $('.sunscreens-item-checkbox').parent().parent().addClass("checked-row");
    } else {
        $('.nav-link').addClass('disabled');
        $('input:submit').prop('disabled', true)
        $('.sunscreens-item-checkbox').parent().parent().removeClass("checked-row");
    }
});

$(".sunscreens-item-checkbox").on('change', function() {
  if (!$(this).prop("checked")) {
    $("#checkAllSunscreens").prop("checked", false);
  }
});


// FUNCTIONS
function showMeasureField(val){ // function to render hidden fields in line item form
  var val = val;

  if (val == 7 || val == 8) { // add center height to models #13 and #15
    $(".height-field").addClass("hidden");
  } else {
    $(".height-field").removeClass("hidden");
  }

  if (val == 6 || val == 8 || val == 13 || val == 15 || val == 11 || val == 18) { // models with 2 pieces
    $(".side-field").removeClass("hidden");
  } else {
    $(".side-field").addClass("hidden");
    $("#id_side").val("");
  }

  if (val == 6 || val == 8 || val == 13 || val == 15 || val == 11 || val == 18 || val == 10 || val == 17) { // models with 2 pieces
    $(".two-piece-exclude-fields").addClass("hidden");
  } else {
    $(".two-piece-exclude-fields").removeClass("hidden");
  }

  if (val == 7 || val == 8 || val == 14 || val == 15) { // add center height to model #14 and #15
    $(".center-height-field").removeClass("hidden");
  } else {
    $(".center-height-field").addClass("hidden");
  }

  if (val > 11) { // add left and right height to models #12 - #15
    $(".lr-height-field").removeClass("hidden");
    $(".left-field").removeClass("hidden");
    $(".right-field").removeClass("hidden");
  } else {
    $(".lr-height-field").addClass("hidden");
  }

  if (val == 13 || val == 15) { // add middle height to models #13 and #15
    $(".middle-height-field").removeClass("hidden");
  } else {
    $(".middle-height-field").addClass("hidden");
  }

  if (val == 4) {
    $(".door-field").removeClass("hidden");
    $(".mount-field").addClass("hidden");
    $(".frame-field").addClass("hidden");
    $(".trim-field").addClass("hidden");
    $("#id_mount").val("");
    $("#id_frame").val(0);
    $("#id_trim_style").val("");
    $(".panel-field").addClass("hidden");
    $(".t-post-field").addClass("hidden");
  } else {
    $(".door-field").addClass("hidden");
    $(".mount-field").removeClass("hidden");
    $(".frame-field").removeClass("hidden");
    $(".trim-field").removeClass("hidden");
    $(".panel-field").removeClass("hidden");
    $(".t-post-field").removeClass("hidden");
  }

};


}); // Document is ready
