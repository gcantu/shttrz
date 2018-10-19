$(function() {

// EVENTS
$('#id_mount').on('change', function() { // show frame field when mount = 'outside'
  var selectedItem = $(this).val();

  if (selectedItem == "Out") {
    $(".frame-field").removeClass("hidden");
  } else {
    $(".frame-field").addClass("hidden");
    $("#id_frame").val(0);
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


// FUNCTIONS


}); // Document is ready
