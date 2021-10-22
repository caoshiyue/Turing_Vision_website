// Boxer plugin
$.widget("ui.boxer", $.extend({}, $.ui.mouse, {

  _init: function() {
    this.element.addClass("ui-boxer");

    this.dragged = false;

    this._mouseInit();

    this.helper = $(document.createElement('div'))
      .css({border:'1px dotted black'})
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
    
    if (x1 > x2) { var tmp = x2; x2 = x1; x1 = tmp; }
    if (y1 > y2) { var tmp = y2; y2 = y1; y1 = tmp; }
    var offsetCanvas = $("#canvas").offset();
	 x2= x2-offsetCanvas.left;
    y2 = y2-offsetCanvas.top;
	 x1= x1-offsetCanvas.left;   
    y1= y1-offsetCanvas.top;

    if (x1<0) {x1=0;}
    if (y1<0) {y1=0;}
    var cWidth = $("#canvas").width();
    if (x2>cWidth) {x2=cWidth;}
    var cHeight = $("#canvas").height();
    if (y2>cHeight) {y2=cHeight;}
    
    
    this.helper.css({left: x1, top: y1, width: x2-x1, height: y2-y1});
    
    this._trigger("drag", event);

    return false;
  },

  _mouseStop: function(event) {
    var self = this;

    this.dragged = false;

    var options = this.options;

    var clone = this.helper.clone()
      .removeClass('ui-boxer-helper').appendTo(this.element);

    this._trigger("stop", event, { box: clone });

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

// Using the boxer plugin
$('#canvas').boxer({
  stop: function(event, ui) {

    var offset = ui.box.offset();
    var offset1 = $("#canvas").offset();
    console.log(offset.left - offset1.left, offset.top-offset1.top, ui.box.width(), ui.box.height());
    ui.box.css({ border: '2px solid black', background: 'rgba(255, 0, 0, 0.5)', 'box-sizing': 'border-box','-moz-box-sizing': 'border-box', '-webkit-box-sizing': 'border-box'});
  }
});
