(function ($) {
    var Message = function (options) {
        options = options || {};
        if (typeof options === "string") {
            options = {
                message: options
            };
        }
        //返回MessageConstructor实例
        return new MessageConstructor(options);
    };
    Message.error = function (options) {
        if (typeof options === "string") {
            options = {
                message: options
            };
        }
        options = $.extend({},options,{type:'error'});
        //返回message实例
        return new MessageConstructor(options);
    };
    Message.warning = function (options) {
        if (typeof options === "string") {
            options = {
                message: options
            };
        }
        options = $.extend({},options,{type:'warning'});
        //返回message实例
        return new MessageConstructor(options);
    };
    Message.info = function (options) {
        if (typeof options === "string") {
            options = {
                message: options
            };
        }
        options = $.extend({},options,{type:'info'});
        //返回message实例
        return new MessageConstructor(options);
    };
    Message.success = function (options) {
        if (typeof options === "string") {
            options = {
                message: options
            };
        }
        options = $.extend({},options,{type:'success'});
        //返回message实例
        return new MessageConstructor(options);
    };
    var MessageConstructor = function (options) {
        this.options = null;
        this.$element = null;
        this.msgId = null;
        this.closed = false;
        this.timer = null;
        this.init(options);
    };
    MessageConstructor.DEFAULT = {
        type: 'info',
        customClass: '',
        duration: 3000,
        message: '',
        showClose: false,
        onClose: null,
        // todo 自定义position
        // position: 'topCenter'
    };
    MessageConstructor.prototype.getDefault = function () {
        return MessageConstructor.DEFAULT;
    }
    MessageConstructor.prototype.getOptions = function (options) {
        return $.extend({}, this.getDefault(), options);
    }
    MessageConstructor.prototype.init = function (options) {
        this.options = this.getOptions(options);
        //生成一个随机5位数，作为id
        var msgId = 'msgId-'
        do msgId += ~~(Math.random() * 100000)
        while (document.getElementById(msgId))
        this.msgId = msgId;
        this.customClass = this.options.customClass;
        this.type = this.options.type;
        this.message = this.options.message;
        var typeImg = "";
        switch (this.type.toLowerCase()) {
            case 'info':
                typeImg = '<i class="fa fa-exclamation-circle text-warning"></i>';
                typeClass = 'info';
                break;
            case 'success':
                typeImg = '<i class="fa fa-check-circle text-success"></i>&nbsp;';
                typeClass = 'success';
                break;
            case 'warning':
                typeImg = '<i class="fa fa-times-circle text-danger"></i>';
                typeClass = 'warning';
                break;
            case 'error':
                typeImg = '<i class="fa fa-times-circle text-danger"></i>';
                typeClass = 'error';
                break;
            default:
                throw new Error('类型必须为["info","success","warning","error"]其中之一')
                break;
        }
        var closeBtn = "";
        if (this.options.showClose) {
            closeBtn = '<div class="jq-message__closeBtn">&times;</div>'
        }
        var msg = '<div class="jq-message begin ' + this.customClass + '" id="' + msgId + '">' +
            '<h3>' + typeImg + this.message  + '</h3>' +
            closeBtn + '</div>';
        $('body').append(msg);
        this.$element = $('#' + msgId);
        this.$closeBtn = this.$element.find('.jq-message__closeBtn');
        var self = this;
        if (this.$closeBtn.length) {
            this.$closeBtn.on('click', function () {
                self.close();
            })
        }

        // 出现时动画,必须要用异步的方法移除类，而且时间必须大于0，否则可能不会有出现动画
        setTimeout(function () {
            self.$element.removeClass('begin');
        }, 10);
        this.startTimer();
        // 鼠标hover事件
        this.$element.hover(function () {
            self.clearTimer();
        }, function () {
            self.startTimer();
        });

    };
    //关闭即销毁
    MessageConstructor.prototype.close = function () {
        var self = this;
        this.closed = true;
        if (typeof this.options.onClose === 'function') {
            this.options.onClose(this);
        }
        //消失动画结束后销毁
        this.$element.addClass('jq-message-fadeOutUp').on('transitionend', function () {
            self.$element.remove();
        });
    };
    MessageConstructor.prototype.clearTimer = function () {
        clearTimeout(this.timer);
    };
    MessageConstructor.prototype.startTimer = function () {
        var self = this;
        var duration = this.options.duration;
        if (duration > 0) {
            this.timer = setTimeout(function () {
                if (!self.closed) {
                    self.close();
                }
            }, duration);
        }
    };
    $.extend({
        message: Message
    });
})(jQuery);