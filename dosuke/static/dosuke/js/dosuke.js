
// クリック状態を把握する
var isClicked = false;

document.onmousedown = function() {
  isClicked = true;
};

document.onmouseup = function() {
  isClicked= false;
};

// クリックした状態でホバーしたら selected にする
$('.form-check-label').mouseenter(function() {
  if (isClicked) {
    const forEle = $(this).attr('for');
    var isChecked = $(`#${forEle}`).prop('checked');
    $(`#${forEle}`).prop('checked', (!isChecked) ? true : false);
  }
});

$('.form-check-label').on('mousedown', function(e) {
  const forEle = $(this).attr('for');
  var isChecked = $(`#${forEle}`).prop('checked');
  $(`#${forEle}`).prop('checked', (!isChecked) ? true : false);
});

$('.form-check-input').on('click', function(e) {
  e.preventDefault();
});

$('.select-all').on('click', function(e) {
  const name = $(this).attr('name');
  $(`.${name}`).prop('checked', true);
});

$('.non-select-all').on('click', function(e) {
  const name = $(this).attr('name');
  $(`.${name}`).prop('checked', false);
});