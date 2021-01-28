/*
    Document   : fobi.plugin.date-bootstrap3-widget.js
    Created on : Apr 26, 2015, 03:30:35 AM
    Author     : Artur Barseghyan (artur.barseghyan@gmail.com)
    Description:
        `bootstrap3` theme date picker plugin scripts.
*/
;

$(document).ready(function() {
    $('input[type="date"]').datetimepicker({
        format: 'YYYY-MM-DD'
    });


//    var dpOptions = {
//        format: 'YYYY-MM-DD',
//        widgetPositioning: {
//            horizontal: 'right',
//            vertical: 'auto'
//        },
//        debug: true,
//        useCurrent: false,
//        widgetParent:'.row'
//    }
//
//    function updatePickers() {
//        var dp = $('input[type="date"]').data('DateTimePicker');
//        dp.options(
//            {
//                format: 'YYYY-MM-DD',
//                widgetPositioning: {
//                    horizontal: 'right',
//                    vertical: 'auto'
//                },
//                debug: true,
//                useCurrent: false,
//                widgetParent:'.row'
//            }
//        )
//    }
//
//
//
//    $('input[type="date"]').datetimepicker(dpOptions).on('dp.change', updatePickers);

//    $('input[type="date"]').datetimepicker({
//        format: 'YYYY-MM-DD',
//        widgetParent: '.row'
//    }).on('dp.show', function(){
//        var top = ($(this).offset().top-300);
//        var left = $(this).offset().left;
//        if($(this).offset().top - 400 <= 0) { //display below if not enough room above
//            top = $(this).offset().top+$(this).height()+10;
//        }
//        $('.bootstrap-datetimepicker-widget').css(
//            {
//            'top':top+'px',
//            'left':left+'px',
//            'bottom':'auto',
//            'right':'auto'
//            }
//        );
//    });

//    $('input[type="date"]').datetimepicker({
//        format: 'YYYY-MM-DD',
////        widgetParent: '.row'
//    }).on('dp.show', function () { // Hack datepicker position
//        var datepicker = $(this).siblings('.bootstrap-datetimepicker-widget');
//
//        var top = ($(this).offset().top-300);
//        var left = $(this).offset().left;
//        if($(this).offset().top - 400 <= 0) { //display below if not enough room above
//            top = $(this).offset().top+$(this).height()+10;
//        }
//
//        if (datepicker.hasClass('top')) {
////            var top = $(this).offset().top - datepicker.height() - 180;
////            datepicker.css({'top': top + 'px', 'bottom': 'auto'});
//            datepicker.css({
//                'top':top+'px',
//                'left':left+'px',
//                'bottom':'auto',
//                'right':'auto'
//            });
//        }
//    });

});
