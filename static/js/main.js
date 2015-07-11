(function($, window, undefined) {
  $(function() {
    $('.modal').on('show.bs.modal', centerModals);
    resizeBoard();
  });

  window.addEventListener("resize", resizeBoard);
  window.addEventListener("resize", centerModals);

  function centerModals(){
    $('.modal').each(function(i){
      var $clone = $(this).clone().css('display', 'block').appendTo('body');
      var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2 - 50);
      top = top > 0 ? top : 0;
      $clone.remove();
      $(this).find('.modal-content').css("margin-top", top);
    });
  }

  function resizeBoard() {
    var $window = $(window);
    var $lists = $("#board_lists");


    var height = $window.height() - $lists.offset().top - 20;
    $("#board_lists").height(height)
  }
})(jQuery, window);