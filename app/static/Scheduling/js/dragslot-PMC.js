;
(function ($, window, document, undefined) {
	var eStart = 'mousedown',
		eMove = 'mousemove',
		eEnd = 'mouseup';

	var clientX, clientY;
	var defaults = {
		slotItemClass: 'slot-item',
		placeholderClass: 'placeholder',
		dragItemClass: 'drag-item',
		slotListClass: 'slot-list',
		slotHandlerClass: 'slot-handler',
		emptySlotClass: 'empty-slot',
		slotClass: 'slot',
		slotItem: 'li',
		slotList: 'ul',
		dropCallback: null
	}

	function Dragslot(element, options) {
		this.element = $(element);
		this.options = $.extend({}, defaults, options);
		this.init();
	}
	Dragslot.prototype = {
		init: function () {
			var slotContainer = this;
			slotContainer.placeholder = $('<div class="' + slotContainer.options.placeholderClass + '"/>');
			var dragStartEvent = function (e) {
				var item = $(e.target);
				if (!item.closest('.' + slotContainer.options.slotItemClass)) {
					return;
				}

				e.preventDefault();
				slotContainer._dragStart(e);

			};
			var dragMoveEvent = function (e) {
				if (slotContainer.dragElement) {
					e.preventDefault();
					slotContainer._dragMove(e);
				}
			};
			var dragEndEvent = function (e) {
				if (slotContainer.dragElement) {
					e.preventDefault();
					slotContainer._dragEnd(e);
				}

			};
			slotContainer.element.on(eStart, dragStartEvent);
			$(window).on(eMove, dragMoveEvent);
			$(window).on(eEnd, dragEndEvent);

		},
		_dragStart: function (e) {
			var target = $(e.target),
				dragItem = target.closest('.' + this.options.slotItemClass);
			this.placeholder.css('height', dragItem.height());
			this.dragElement = $(document.createElement('div')).addClass(this.options.dragItemClass);
			this.slotlist = target.closest('.' + this.options.slotListClass);
			dragItem.after(this.placeholder);
			// dragItem.css('width',dragItem.width() + 'px');
			// dragItem.css('background-color: #337AB7;');
			if (dragItem[0].parentNode) {
				dragItem[0].parentNode.removeChild(dragItem[0]);
			}
			dragItem.appendTo(this.dragElement);
			$(document.body).append(this.dragElement);
			clientX = e.clientX + (document.body.scrollLeft || document.documentElement.scrollLeft);
			clientY = e.clientY + (document.body.scrollTop || document.documentElement.scrollTop);
			this.dragElement.css({
				'left': clientX,
				'top': clientY
			});
			if (dragItem.hasClass("currentli")) {
				dragItem.removeClass("currentli");
			} else {
				dragItem.addClass("currentli");
			}

		},
		_dragMove: function (e) {
			var newClientX = e.clientX + (document.body.scrollLeft || document.documentElement.scrollLeft),
				newClientY = e.clientY + (document.body.scrollTop || document.documentElement.scrollTop);
			var left = parseInt(this.dragElement[0].style.left) || 0;
			var top = parseInt(this.dragElement[0].style.top) || 0;
			this.dragElement[0].style.left = left + (newClientX - clientX) + 'px';
			this.dragElement[0].style.top = top + (newClientY - clientY) + 'px';
			clientX = newClientX;
			clientY = newClientY;

			this.dragElement[0].style.visibility = 'hidden';
			this.pointEl = $(document.elementFromPoint(e.pageX - (document.body.scrollLeft || document.documentElement.scrollLeft), e.pageY - (document.body.scrollTop || document.documentElement.scrollTop)));

			this.dragElement[0].style.visibility = 'visible';

			if (this.pointEl.closest('.' + this.options.slotHandlerClass).length || this.pointEl.closest('.' + this.options.slotItemClass).length) {
				this.pointEl = this.pointEl.closest('.' + this.options.slotItemClass);
				var before = e.pageY < (this.pointEl.offset().top + this.pointEl.height() / 2);
				parent = this.placeholder.parent();

				if (before) {
					this.pointEl.before(this.placeholder);
				} else {
					this.pointEl.after(this.placeholder);
				}
			} else if (this.pointEl.hasClass(this.options.emptySlotClass)) {
				list = $(document.createElement(this.options.slotList)).addClass(this.options.slotListClass);
				list.append(this.placeholder);
				this.pointEl.append(list);
			} else if (this.pointEl.hasClass(this.options.slotClass)) {
				this.pointEl = this.pointEl.children(this.options.slotList).children().last();
				this.pointEl.after(this.placeholder);
			} else {
				return;
			}
			this.toSlot = this.pointEl.closest('.' + this.options.slotClass);

		},
		_dragEnd: function (e) {
			var self = this;
			var el = self.dragElement.children('.' + self.options.slotItemClass).first();
			el[0].parentNode.removeChild(el[0]);
			this.placeholder.replaceWith(el);
			self.dragElement.remove();
			if ($.isFunction(self.options.dropCallback)) {
				var itemInfo = {
					dragItem: el,
					sourceSlot: self.slotlist.closest('.slot'),
					destinationSlot: self.toSlot,
					dragItemId: el.attr('id')
				}
				self.options.dropCallback.call(self, itemInfo);
			}
			self.dragElement = null;
			self.pointEl = null;
			if (self.toSlot.hasClass(self.options.emptySlotClass)) {
				self.toSlot.removeClass(self.options.emptySlotClass);
			}
			if (self.slotlist.children().length == 0) {
				self.slotlist.closest('.' + self.options.slotClass).addClass(self.options.emptySlotClass);
				// self.slotlist[0].parentNode.removeChild(self.slotlist[0]);
			}
			console.log('22222222222222')
			AJAXData(el);
		}
	}


	$.fn.dragslot = function (options) {
		new Dragslot(this, options);
	}

	var AJAXData = function () {
		var ReturnList = [];
		var topli = $$('top-div').children[0].children;
		var LiList = topli;
		var Working = GetCurrentWork();
		console.log(Working)
		// console.log(LiList)
		for (var i = 0; i < LiList.length; i++) {
			// console.log(LiList[i])
			var uppTrackJobGUID = LiList[i].children[0].children[0].children[0].children[0].children[0].children[16].innerText;
			console.log(uppTrackJobGUID)
			var tdDict = {
				'uppTrackJobGUID': uppTrackJobGUID,
				'sType': Working,
				'nRowNumber': i,
			}
			if (uppTrackJobGUID != '') {
				ReturnList.push(tdDict);
			}
		}
		console.log('ReturnList')
		console.log(ReturnList)
		$.ajax({
			type: 'POST',
			url: 'ZL/AJAX/Move',
			data: JSON.stringify(ReturnList),
			contentType: 'application/json; charset=UTF-8',
			dataType: 'json',
			success: function (ReturnList) {
				// AjaxPage();
			},
		});
		console.log(111)
		getCount();
		// $('#top-div').load('AJAX/page');
		// console.log(LiList)

	}


})(window.jQuery, window, document);