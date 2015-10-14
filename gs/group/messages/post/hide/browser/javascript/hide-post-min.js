"use strict";jQuery.noConflict();function GSHidePost(g,f,e){var c=null,h=null,b=null,i="../hide_post.ajax";
function j(m){var l="";l=jQuery(this).data("post-id");h.data("postId",l);h.modal("show")
}function k(m){var l=null;l=jQuery(this).data("postId");b.load(i,{"form.postId":l},d)
}function d(n,m,o){var l=null;l=jQuery("#form\\.actions\\.hide");l.button()}function a(){c=jQuery(g);
h=jQuery(f);b=jQuery(e)}a();return{init:function(){c.click(j);h.on("shown",k)}}}jQuery(window).load(function(){var a=null;
a=GSHidePost(".hide-button","#hide-the-post","#hide-the-post-loading");a.init()});