/**
 * Created by Administrator on 2017/8/20 0020.
 */
window.onload = function() {
    var headerNav = document.getElementsByClassName('buttons')[0];
    var navbtns = headerNav.getElementsByTagName('a');

    var searchInput = document.getElementById('searchInput');

    var postList = document.getElementsByClassName('post-box');

    for (var i=1; i<navbtns.length; i++) {
      navbtns[i].onclick = function() {
        for (var j=1; j<navbtns.length; j++) {
          navbtns[j].className = '';
        }
        this.className = 'current';
      }
    }

    navbtns[0].onclick = function() {

    };
    // searchInput.onclick = function() {
    //   this.style.borderLeft = "2px solid #df846c;"
    // }
    // post-list onmouseover
    for (var a=0; a<postList.length; a++) {
      postList[a].onmouseover = function() {
        this.style.boxShadow = "2px 2px 5px #d3d6da";
      };
      postList[a].onmouseout = function() {
        this.style.boxShadow = "";
      }
    }
  };