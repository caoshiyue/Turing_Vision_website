$(document).ready(function($) {
    //var hostip = 'http://127.0.0.1:8000'
    var hostip = 'http://visionturing.shiyuec.cn' //上线修改
        //-------------------------------------------------------------
        // 
        // Plugin
        //http://jsfiddle.net/h8vnw/
        //-------------------------------------------------------------
    $.widget("ui.boxer", $.extend({}, $.ui.mouse, {

        _init: function() {
            this.element.addClass("ui-boxer");

            this.dragged = false;

            this._mouseInit();

            this.helper = $(document.createElement('div'))
                .css({
                    border: '1px dotted white'
                })
                .addClass("ui-boxer-helper");
        },

        destroy: function() {
            this.element
                .removeClass("ui-boxer ui-boxer-disabled")
                .removeData("boxer")
                .unbind(".boxer");
            this._mouseDestroy();

            return this;
        },

        _mouseStart: function(event) {
            var self = this;
            var offsetCanvas = $("#output").offset();
            var cWidth = $("#output").width() + offsetCanvas.left;
            var cHeight = $("#output").height() + offsetCanvas.top;


            this.opos = [Math.min(event.clientX, cWidth), Math.min(event.clientY, cHeight)];

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

        _mouseDrag: function(event) {
            var self = this;
            this.dragged = true;

            if (this.options.disabled)
                return;

            var options = this.options;

            var x1 = this.opos[0];
            var y1 = this.opos[1];
            var x2 = event.clientX;
            var y2 = event.clientY;
            var offsetCanvas = $("#output").offset();

            var cWidth = $("#output").width() + offsetCanvas.left;
            var cHeight = $("#output").height() + offsetCanvas.top;

            if (x1 > cWidth)
                return;
            if (y1 > cHeight)
                return;

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
            // x2 = x2 - offsetCanvas.left;
            // y2 = y2 - offsetCanvas.top;
            // x1 = x1 - offsetCanvas.left;
            // y1 = y1 - offsetCanvas.top;

            if (x1 < offsetCanvas.left) {
                x1 = offsetCanvas.left;
            }
            if (y1 < offsetCanvas.top) {
                y1 = offsetCanvas.top;
            }
            if (x2 > cWidth) {
                x2 = cWidth;
            }
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

        _mouseStop: function(event) {
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
        var t = document.createTextNode(markN); // Create a text node
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
        var delete_btn = document.getElementById("delLast")
        delete_btn.style['display'] = 'block'
        var newdiv = document.createElement('div');
        newdiv.setAttribute("id", "tag" + markN)
        newdiv.innerHTML = "Marker " + (markN) + " <br><input type='text' readonly='readonly' id='formInput" + (markN) + "' name='myInput" + (markN) + "'>";
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

        data.forEach(function(item) {
            ctr = 0;
            keys.forEach(function(key) {
                if (ctr > 0) result += columnDelimiter;

                result += item[key];
                ctr++;
            });
            result += lineDelimiter;
        });

        return result;
    }

    function nextImg(imgN, image, label) {
        var output = document.querySelector('#output');
        output.style["max-height"] = document.body.clientHeight * 0.8 + 'px'
        output.src = image
        document.getElementById('label').innerHTML = label

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
        if (json_image.name == undefined)
            return
        var json_obj = new Object();
        json_obj.image_path = json_image.name;
        json_obj.category = parseInt(json_image.label)
            //json_obj.usr = rater
        json_obj.times_of_test = times_of_test
        json_obj.width = $('#output').width();
        json_obj.height = $('#output').height();
        var points = new Object();
        for (i in markerList) {
            var point = new Object();
            point.X = cListX[i];
            point.Y = cListY[i];
            point.W = cListW[i];
            point.H = cListH[i];
            points[i] = point
        }
        json_obj.points = points
        post_annotation(json_obj)
    }

    function post_annotation(json_obj) {
        var httpRequest = new XMLHttpRequest(); //第一步：创建需要的对象
        httpRequest.open('POST', hostip + '/anno/', true);
        httpRequest.setRequestHeader("Content-type", "application/json"); //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };
        httpRequest.send(JSON.stringify(json_obj)); //发送请求 将json写入send中

        httpRequest.onreadystatechange = function() { //请求后的回调接口，可将请求成功后要执行的程序写在其中
            if (httpRequest.readyState == 4 && httpRequest.status == 200) { //验证请求是否发送成功
            }
        };
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

    var times_of_test = 0
    var imgN = -1;

    var markN = 1;
    var cListX = [];
    var cListY = [];
    var cListW = [];
    var cListH = [];
    var totalList = [];
    var boxMode = true;
    var is_instruction_img = true;
    var imList_lenth = 1;
    var scaleWarning = false;
    var scaleto = false;
    var json_image = [];

    $('.modal').modal('show');

    $('#file-input').change(function(files) {
        reset();
        imgN = 0;
        nextImg(imgN);
    });

    function checkradio() {
        var radio = document.getElementsByName("timesoftest");
        for (var i = 0; i < 2; i++) {
            if (radio[i].checked) { //radio按钮使用checked作为是否被选中的判断条件，true表示被选中
                select = radio[i].value; //获取被选中radio的值
            }
        }
        return select

    }

    function get_num_image(r, p) {
        var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
        msg = 'p=' + p
        httpRequest.open('GET', hostip + '/number/?' + msg, true);
        httpRequest.send();
        httpRequest.onreadystatechange = function() {
            if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                var json = httpRequest.responseText;
                imList_lenth = parseInt(json)

            }
        };
    }

    window.onload = function() {
        setProgressBar(0);
        boxMode = true;
        console.log(boxMode)

        times_of_test = 1 //checkradio()
        get_num_image(undefined, times_of_test)

        console.log("collected data");
        $('.modal').modal("hide");
        //nextImg(imgN);
        // return false

        console.log("box", boxMode);

        if (boxMode) {


            // Using the boxer plugin
            $('#canvas').boxer({
                stop: function(event, ui) {

                    var offset = ui.box.offset();
                    var offset1 = $("#canvas").offset();

                    var x = Math.round(offset.left - offset1.left);
                    var y = Math.round(offset.top - offset1.top);
                    var w = Math.round(ui.box.width());
                    var h = Math.round(ui.box.height());

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
                    document.getElementById("formInput" + markN.toString()).value = [x, y, w, h].toString();
                    $("#formInput" + markN).focus()

                    markN = markN + 1;
                    if (markN > 6 || is_instruction_img) {
                        $("#delLast").click()
                        return false;
                    }
                }
            });
        } else {
            console.log("spotty version")
            $('#output').bind('click', function(ev) {
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
    };

    // $('#nextButton').click(function () {
    document.getElementById("nextButton").onclick = function() {
            is_instruction_img = false
            collectPictureAnnotations();
            if (imgN + 1 >= imList_lenth) {
                alert("你已经完成了测试")
                return
            }

            var httpRequest = new XMLHttpRequest(); //第一步：建立所需的对象
            //p=[0,1,2]
            msg = 'imgid=' + (imgN + 1).toString() + '&p=' + times_of_test
            httpRequest.open('GET', hostip + '/next/?' + msg, true);
            httpRequest.send(); //第三步：发送请求  将请求参数写在URL中
            /**
             * 获取数据后的处理程序
             */
            httpRequest.onreadystatechange = function() {
                if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                    imgN = imgN + 1;
                    setProgressBar(imgN);
                    var json = httpRequest.responseText; //获取到json字符串，还需解析
                    console.log(json);
                    json_image = jQuery.parseJSON(json);
                    class_name = json_image.label.category_name_cn;
                    nextImg(imgN, json_image.image_base64_string, class_name);
                    reset();
                    var delete_btn = document.getElementById("delLast")
                    delete_btn.style['display'] = 'none'
                }
            };

        }
        // );

    /*window.onbeforeunload = function(e) {
        var dialogText = 'Dialog text here';
        e.returnValue = dialogText;
        return dialogText;
    };*/

    $("#delLast").click(function() {
        if (markN >= 2) {
            removeMarker(markN, cListX, cListY, cListW, cListH);
            markN = markN - 1;
        }
        if (markN < 2) {
            var delete_btn = document.getElementById("delLast")
            delete_btn.style['display'] = 'none'
        }
    });

}); //document.ready()