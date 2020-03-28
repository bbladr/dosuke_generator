
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
// チェックボックスをクリックした時の挙動
$('.form-check-label').on('mousedown', function(e) {
  const forEle = $(this).attr('for');
  var isChecked = $(`#${forEle}`).prop('checked');
  $(`#${forEle}`).prop('checked', (!isChecked) ? true : false);
});
$('.form-check-input').on('click', function(e) {
  e.preventDefault();
});

// バンド内全選択
$('.select-all').on('click', function(e) {
  const name = $(this).attr('name');
  $(`.${name}`).prop('checked', true);
});

// バンド内全解除
$('.non-select-all').on('click', function(e) {
  const name = $(this).attr('name');
  $(`.${name}`).prop('checked', false);
});

// 一括選択
$('.global-select-all').on('click', function(e) {
  const name = $(this).attr('name');
  $(`.${name}`).prop('checked', true);
})

// 一括解除
$('.global-non-select-all').on('click', function(e) {
  const name = $(this).attr('name');
  $(`.${name}`).prop('checked', false);
})

// 土スケ生成待機中の表示
function dispLoading(msg){
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

// 設定更新アラートの時限非表示
setTimeout(function(){
  $('.appear-2s').addClass("d-none");
},2000);