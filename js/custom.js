(function ($) {

    new WOW().init();
    var previous_events_url = "/index.php?title=Special:Ask/-5B-5BCategory:Event-5D-5D-20-5B-5BEvent-20status::Ready-5D-5D-20-5B-5BDate::-3C2015-2D01-2D19T00:00:00-5D-5D/-3FDate/-3FPlace/format%3Djson/limit%3D2/sort%3DDate/order%3Ddescending/default%3DNo-20past-20event./offset%3D0";
    var next_events_url = "/index.php?title=Special:Ask/-5B-5BCategory:Event-5D-5D-20-5B-5BEvent-20status::Ready-5D-5D-20-5B-5BDate::-3E2015-2D01-2D19T00:00:00-5D-5D/-3FDate/-3FPlace/format%3Djson/limit%3D10/sort%3DDate/order%3Dascending/default%3DNo-20upcoming-20event./offset%3D0";


    jQuery(window).load(function() {
        jQuery("#preloader").delay(100).fadeOut("slow");
        jQuery("#load").delay(100).fadeOut("slow");
    });


    //jQuery to collapse the navbar on scroll
    $(window).scroll(function() {
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
        }
    });


    //jQuery to inline SVG so it's stylable which makes me so happy
    /*
     * http://stackoverflow.com/questions/11978995/how-to-change-color-of-svg-image-using-css-jquery-svg-image-replacement
     * Replace all SVG images with inline SVG
     */
    jQuery('img.svg').each(function(){
    	var $img = jQuery(this);
        var imgID = $img.attr('id');
        var imgClass = $img.attr('class');
        var imgURL = $img.attr('src');

        jQuery.get(imgURL, function(data) {
            // Get the SVG tag, ignore the rest
            var $svg = jQuery(data).find('svg');

            // Add replaced image's ID to the new SVG
            if(typeof imgID !== 'undefined') {
                $svg = $svg.attr('id', imgID);
            }
            // Add replaced image's classes to the new SVG
            if(typeof imgClass !== 'undefined') {
                $svg = $svg.attr('class', imgClass+' replaced-svg');
            }

            // Remove any invalid XML tags as per http://validator.w3.org
            $svg = $svg.removeAttr('xmlns:a');

            // Replace image with new SVG
            $img.replaceWith($svg);

        }, 'xml');

    });
	

    function addMeetings(url, kind) {
        var element = $("#" + kind + "-meetings");
        $.getJSON(url).success(function(data){
            if ($.isEmptyObject(data.results)) {
                // will only happen for next meeting *normally* (haha.)
                element.html('<p class="meeting"><i>There is no next meeting planned yet</i></p>')
            } else {
                // this is horrible, I do this because data is not in a list but is sorted on the object
                // semantic merdiawiki really have a shitty export
                for (i in data.results) {
                    var url = data.results[i].fullurl;
                    var location = data.results[i].printouts.Place[0]
                    var date = new Date(data.results[i].printouts.Date[0] * 1000);
                    // javascript is super lame
                    var month = date.getMonth() + 1;
                    if (month < 10) {
                        var month = "0" + month;
                    }
                    var date = date.getDate() + "/" + month + "/" + date.getUTCFullYear();
                    element.append('<p class="meeting">' + date + ' - <a href="' + window.location.protocol + url + '"><b>' + i.slice(6, i.length) + '</b></a> ' + location + '</p>')
                }
            }
        }).error(function(data) {
            console.log("Can't get " + kind + " meetings: ");
            console.log(data);
            element.html('<p class="meeting"><i>There is no next meeting planned yet</i></p>')
        })
    }

    //jQuery for page scrolling feature - requires jQuery Easing plugin
    $(function() {
        addMeetings(previous_events_url, "previous");
        addMeetings(next_events_url, "next");
        $('.navbar-nav li a').bind('click', function(event) {
            var $anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top
            }, 1500, 'easeInOutExpo');
            event.preventDefault();
        });
        $('.page-scroll a').bind('click', function(event) {
            var $anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top
            }, 1500, 'easeInOutExpo');
            event.preventDefault();
        });
    });

})(jQuery);
