
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

$('.global-select-all').on('click', function(e) {
  $(`.form-check-input`).prop('checked', true);
})

$('.global-non-select-all').on('click', function(e) {
  $(`.form-check-input`).prop('checked', false);
})

function dispLoading(msg){
  // 引数なし（メッセージなし）を許容
  if( msg == undefined ){
    msg = "";
  }
  // 画面表示メッセージ
  var dispMsg = "<div class='loadingMsg'>" + msg + "</div>";
  // ローディング画像が表示されていない場合のみ出力
  if($("#loading").length == 0){
    $("body").append("<div id='loading'>" + dispMsg + "</div>");
  }
}

$(function () {
  $(".btn-generate").click( function() {
    dispLoading("土スケ生成中...");
  });
});

setTimeout(function(){
  $('.appear-2s').addClass("d-none");
},2000);