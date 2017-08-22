// Always js

$(function() {
  // 导航栏点击效果
  $('.buttons a:gt(0)').click(function() {
    $('.buttons a:gt(0)').removeClass();
    $(this).attr('class', 'current');
  });

  // 首页文章box效果
  $('.post-box').mouseenter(function() {
    $(this).css('boxShadow', '2px 2px 5px #d3d6da');
  });
  $('.post-box').mouseleave(function() {
    $(this).css('boxShadow', '');
  });

  // button go to top
  $(function() {
    $(window).scroll(function() {
      if ($(window).scrollTop() > 100) {
        $('#go-to-top').fadeIn(1000);
        $('#go-to-top').css('left', (Math.max(document.body.clientWidth, 960) - 960) / 2 + 690);
      } else {
        $('#go-to-top').fadeOut(1000);
      }
    });

    $('#go-to-top').click(function() {
      $('html, body').animate({scrollTop: 0}, 1000);
      return false;
    });
  });

})

$(function() {
  // 移动端导航按钮
  $('.menu-btn').click(function() {
    if ($('#menu').css('display') === 'none') {
      $('#menu').css('display', 'block');
    } else {
      $('#menu').css('display', 'none');
    }
  });
  // 搜索框
  $('#menu .menu-list .list:first-child').click(function() {
    $('#mob-search').css('display', 'block');
  });
  $('#mob-search #cancel').click(function() {
    $('#mob-search').css('display', 'none');
  })
})
