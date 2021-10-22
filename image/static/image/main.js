$(document).ready(function ($) {
    //var hostip = 'http://127.0.0.1:8000'
    var hostip = 'http://anno.shiyuec.cn' //上线修改
    //-------------------------------------------------------------
    // 
    // Plugin
    //http://jsfiddle.net/h8vnw/
    //-------------------------------------------------------------
    $.widget("ui.boxer", $.extend({}, $.ui.mouse, {

        _init: function () {
            this.element.addClass("ui-boxer");

            this.dragged = false;

            this._mouseInit();

            this.helper = $(document.createElement('div'))
                .css({
                    border: '1px dotted white'
                })
                .addClass("ui-boxer-helper");
        },

        destroy: function () {
            this.element
                .removeClass("ui-boxer ui-boxer-disabled")
                .removeData("boxer")
                .unbind(".boxer");
            this._mouseDestroy();

            return this;
        },

        _mouseStart: function (event) {
            var self = this;

            this.opos = [event.clientX, event.clientY];

            if (this.options.disabled)
                return;

            var options = this.options;

            this._trigger("start", event);

            //    $(options.appendTo).append(this.helper);
            $('#canvas').append(this.helper);

            this.helper.css({
                "z-index": 100,
                "position": "absolute",
                "left": event.clientX,
                "top": event.clientY,
                "width": 0,
                "height": 0
            });
        },

        _mouseDrag: function (event) {
            var self = this;
            this.dragged = true;

            if (this.options.disabled)
                return;

            var options = this.options;

            var x1 = this.opos[0];
            var y1 = this.opos[1];
            var x2 = event.clientX;
            var y2 = event.clientY;

            if (x1 > x2) {
                var tmp = x2;
                x2 = x1;
                x1 = tmp;
            }
            if (y1 > y2) {
                var tmp = y2;
                y2 = y1;
                y1 = tmp;
            }
            var offsetCanvas = $("#canvas").offset();
            x2 = x2 - offsetCanvas.left;
            y2 = y2 - offsetCanvas.top;
            x1 = x1 - offsetCanvas.left;
            y1 = y1 - offsetCanvas.top;

            if (x1 < 0) {
                x1 = 0;
            }
            if (y1 < 0) {
                y1 = 0;
            }
            var cWidth = $("#canvas").width();
            if (x2 > cWidth) {
                x2 = cWidth;
            }
            var cHeight = $("#canvas").height();
            if (y2 > cHeight) {
                y2 = cHeight;
            }


            this.helper.css({
                left: x1,
                top: y1,
                width: x2 - x1,
                height: y2 - y1
            });

            this._trigger("drag", event);

            return false;
        },

        _mouseStop: function (event) {
            var self = this;

            this.dragged = false;

            var options = this.options;

            var clone = this.helper.clone()
                .removeClass('ui-boxer-helper').appendTo(this.element);

            this._trigger("stop", event, {
                box: clone
            });

            this.helper.remove();

            return false;
        }

    }));

    $.extend($.ui.boxer, {
        defaults: $.extend({}, $.ui.mouse.defaults, {
            appendTo: 'body',
            distance: 0
        })
    });

    //-------------------------------------------------------------
    // 
    // Make Markers
    //
    //-------------------------------------------------------------

    function makeMarker(coX, coY, markN) {
        var m = document.createElement("div");
        m.setAttribute("class", "marker");
        var idName = "marker" + markN;
        m.setAttribute("id", idName);
        var t = document.createTextNode(markN);    // Create a text node
        m.appendChild(t);
        var canvas = document.getElementById("canvas");
        canvas.appendChild(m);
        coY = coY - 10;
        coX = coX - 10;
        $("#" + idName).css({ "top": coY + "px", "left": coX + "px" });
        //	 document.getElementById(idName).style.top = coY+"px";
        addTag(markN);
        document.getElementById("formInput" + markN).focus()
    }



    function addTag(markN) {
        var newdiv = document.createElement('div');
        newdiv.setAttribute("id", "tag" + markN)
        newdiv.innerHTML = "Marker " + (markN) + " <br><input type='text' id='formInput" + (markN) + "' name='myInput" + (markN) + "'>";
        document.getElementById("dynamicInput").appendChild(newdiv);
    }

    function removeMarker(markN, cListX, cListY, cListW, cListH) {
        //remove Tag
        markN = markN - 1
        var tagDel = document.getElementById("tag" + (markN))
        tagDel.parentNode.removeChild(tagDel);
        //remove marker
        var markDel = document.getElementById("marker" + (markN))
        markDel.parentNode.removeChild(markDel);
        cListX.pop();
        cListY.pop();
        cListW.pop();
        cListH.pop();
    }

    function obj2csv(args) {
        var result, ctr, keys, columnDelimiter, lineDelimiter, data;

        data = args.data || null;
        if (data == null || !data.length) {
            return null;
        }

        columnDelimiter = args.columnDelimiter || ',';
        lineDelimiter = args.lineDelimiter || '\n';

        keys = Object.keys(data[0]);

        result = '';
        result += keys.join(columnDelimiter);
        result += lineDelimiter;

        data.forEach(function (item) {
            ctr = 0;
            keys.forEach(function (key) {
                if (ctr > 0) result += columnDelimiter;

                result += item[key];
                ctr++;
            });
            result += lineDelimiter;
        });

        return result;
    }

    function nextImg(imgN, image) {
        var output = document.querySelector('#output');
        // Adjust the canvas size only after the image has completetly loaded
        // output.onload = function () {
        //     var outputWidth = $(this).width(),
        //         outputHeight = $(this).height();
        //     $("#canvas").css({
        //         width: outputWidth,
        //         height: outputHeight
        //     });
        // }
        // //var image = document.querySelector('#file-input').files[imgN];

        // var maxh = $(window).height() - 150;
        // var maxw = $(window).width() - 350;
        // if (scaleto) {
        //     var maxh = 960;
        //     var maxw = 1200;
        // }

        // $("#output").css({
        //     "max-width": maxw,
        //     "max-height": maxh
        // });

        //output.src = URL.createObjectURL(image);
        output.src = image
        // if (!scaleWarning) {
        //     if (maxh < $("#output").prop("naturalHeight") || maxw < $("#output").prop("naturalWidth")) {
        //         console.log("scale")
        //         alert("This screen can only display images of up to " + maxh + "px x" + maxw + ". The image will be displayed scaled down.");
        //         scaleWarning = true;
        //     }
        // }
    }

    function save(ls, fname) {
        var data, filename, link, ls;
        var csv = obj2csv({
            data: ls
        });
        filename = fname || 'export.csv';
        if (!csv.match(/^data:text\/csv/i)) {
            csv = 'data:text/csv;charset=utf-8,' + csv;
        }
        data = encodeURI(csv);
        link = document.createElement('a');
        link.setAttribute('href', data);
        link.setAttribute('download', fname);
        link.click();
    }

    function downloadCSV(totalList, rater) {
        var a = document.createElement('a');
        var csvString = obj2csv({
            data: totalList
        });
        a.href = 'data:attachment/csv,' + encodeURIComponent(csvString);
        a.target = '_blank';
        var fname = "Ratings" + rater + ".csv"
        a.download = fname;
        document.body.appendChild(a);
        a.click();
    }

    function reset() {
        // reset stuff
        markN = 1;
        cListX = [];
        cListY = [];
        cListW = [];
        cListH = [];
        $("#canvas").children(":not(#output)").remove();
        $("#dynamicInput").empty();
    }

    function arrayTrim(ar) {
        for (i in ar) {
            ar[i].value = ar[i].value.trim();
        }
        return ar
    }


    function collectPictureAnnotations() {

        var markerList = $('#wholeForm').serializeArray();
        markerList = arrayTrim(markerList);
        for (i in markerList) {
            markerList[i].rater = rater;
            markerList[i].X = cListX[i];
            markerList[i].Y = cListY[i];
            markerList[i].W = cListW[i];
            markerList[i].H = cListH[i];
            markerList[i].image = json_image.name;
            markerList[i].imgSizeX = $('#output').width();
            markerList[i].imgSizeY = $('#output').height();
        }
        $.merge(totalList, markerList);
        console.log(markerList);
        var csv = obj2csv({ data: totalList });
        console.log(csv);
    }

    function setProgressBar(n) {
        var total = imList_lenth;
        if (n == total) return
        n += 1;
        var percProg = (n / total) * 100;
        $('.progress-bar').css('width', percProg + '%').attr('aria-valuenow', percProg);
        $('#progress-indicator').text(n + ' / ' + total);
    }

    //-------------------------------------------------------------
    // 
    // Actual Script
    //
    //-------------------------------------------------------------

    var debug = true;

    var rater = debug ? 'debug' : window.prompt("Username:", " ");
    var times_of_test = 0
    var imgN = -1;

    var markN = 1;
    var cListX = [];
    var cListY = [];
    var cListW = [];
    var cListH = [];
    var totalList = [];
    var boxMode = true;
    var imList_lenth = 128;
    var scaleWarning = false;
    var scaleto = false;
    var json_image = [];
    $('.modal').modal('show');

    $('#file-input').change(function (files) {
        reset();
        imgN = 0;
        nextImg(imgN);
    });

    function get_num_image(r, p) {
        var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
        msg = 'user=' + r + '&p=' + p
        httpRequest.open('GET', hostip + '/number/?' + msg, true);
        httpRequest.send();
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                var json = httpRequest.responseText;
                imList_lenth = parseInt(json)

            }
        };
    }
    window.onload = function () {
        setProgressBar(0);
        boxMode = true;
        console.log(boxMode)
        rater = 'train';
        get_num_image(rater, 'train')

        console.log("collected data");
        $('.modal').modal("hide");
        //nextImg(imgN);
        // return false

        console.log("box", boxMode);

        if (boxMode) {


            // Using the boxer plugin
            $('#canvas').boxer({
                stop: function (event, ui) {

                    var offset = ui.box.offset();
                    var offset1 = $("#canvas").offset();

                    var x = offset.left - offset1.left;
                    var y = offset.top - offset1.top;
                    var w = ui.box.width();
                    var h = ui.box.height();

                    cListX.push(x);
                    cListY.push(y);
                    cListW.push(w);
                    cListH.push(h);

                    console.log(x, y, w, h);
                    ui.box.addClass("mBox");

                    var idName = "marker" + markN;
                    ui.box.attr("id", idName);
                    var t = document.createTextNode(markN); // Create a text node
                    ui.box.append(t);

                    addTag(markN);
                    $("#formInput" + markN).focus()

                    markN = markN + 1;
                }
            });
        }
        else {
            console.log("spotty version")
            $('#output').bind('click', function (ev) {
                var $div = $(ev.target);
                console.log($div)
                var offset1 = $div.offset();
                var x = ev.clientX - offset1.left;
                var y = ev.clientY - offset1.top;
                cListX.push(x);
                cListY.push(y);
                console.log('x: ' + x + ', y: ' + y);
                makeMarker(x, y, markN);
                markN = markN + 1;
            });
        }
        return false
    }

    // $('#nextButton').click(function () {
    document.getElementById("nextButton").onclick = function () {
        collectPictureAnnotations();
        if (imgN + 1 >= imList_lenth) {
            alert("学习结束")
            return
        }

        var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
        //p=[0,1,2]
        msg = 'user=' + rater + '&imgid=' + (imgN + 1).toString() + '&p=' + 'train'
        httpRequest.open('GET', hostip + '/next/?' + msg, true);
        httpRequest.send();//第三步：发送请求  将请求参数写在URL中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                imgN = imgN + 1;
                setProgressBar(imgN);
                var json = httpRequest.responseText;//获取到json字符串，还需解析
                console.log(json);
                json_image = jQuery.parseJSON(json);
                nextImg(imgN, json_image.image_base64_string);
                reset();
            }
        };

    }
    // );

    /*window.onbeforeunload = function(e) {
        var dialogText = 'Dialog text here';
        e.returnValue = dialogText;
        return dialogText;
    };*/

    $('#lastButton').click(function () {
        collectPictureAnnotations();
        if (imgN <= 0)
            return


        var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
        //p=[0,1,2]
        msg = 'user=' + rater + '&imgid=' + (imgN - 1).toString() + '&p=' + 'train'
        httpRequest.open('GET', hostip + '/next/?' + msg, true);
        httpRequest.send();//第三步：发送请求  将请求参数写在URL中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                imgN = imgN - 1;
                setProgressBar(imgN);
                var json = httpRequest.responseText;//获取到json字符串，还需解析
                console.log(json);
                json_image = jQuery.parseJSON(json);
                nextImg(imgN, json_image.image_base64_string);
                reset();
            }
        };
    });

    $("#delLast").click(function () {
        if (markN < 2) {
            return
        } else {
            removeMarker(markN, cListX, cListY, cListW, cListH);
            markN = markN - 1;
        }
    });

}); //document.ready()