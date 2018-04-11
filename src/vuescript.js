var host = 'http://130.89.138.226:8000'

var ColorPicker = new iro.ColorPicker("#color-picker-container", {
    width: 320,
    height: 320,
    color: {r: 255, g: 0, b: 0, a: 0},
    markerRadius: 8,
    padding: 4,
    sliderMargin: 24,
    sliderHeight: 36,
    borderWidth: 2,
    borderColor: "#fff",
    anticlockwise: true,
});

ColorPicker.on("mount", function (color) {
    ColorPicker.color.rgb = vm.getColor();
});

ColorPicker.on("input:end", function (color) {
    vm.setColor(color.rgb);
});

var vm = new Vue({
    el: '#app',
    template: '#main-page',
    data: {
        'player': {
            'mode' : 'bluetooth',
            'status': 'No Status',
            'volume': 0,
            'artist': 'No Data',
            'title': 'No Data',
            'albumCover': 'http://i0.kym-cdn.com/entries/icons/facebook/000/007/333/276751_119503071478225_2986698_n.jpg',
            'totalTime': '99:99',
            'currentTime': '00:00',
            'elapsedTime': 0,
            'LEDon': true
        },
        'LED': {
            rgba: {r: 255, g: 255, b: 255}
        },
        spdVisible: true,
        spdOpen: false,
        shareItems: {
            'bluetooth': 'fa-bluetooth',
            'youtube': 'fa-youtube',
        }
    }
    ,

    created: function () {
        this.fetchData();
    },

    methods: {
        fetchData: function () {
            this.$http.get(host + '/player')
                .then(response => {
                this.player = response.body[0]

        })
            ;
            this.$http.get(host + '/led')
                .then(response => {
                this.LED.rgba = response.body[0]

        })
            ;
        },

        getColor: function () {
            return this.LED.rgba;
        },

        setColor: function(rgb) {
            this.LED.rgba = rgb;
            this.sendDataLED();
        },

        sendDataPlayer: function () {
            this.$http.post(host + '/player', this.player)
        },

        sendDataLED: function () {
            this.$http.post(host + '/led', this.LED.rgba)
        },

        setMode: function (Name) {
            this.player.mode = Name;
            this.sendDataPlayer();
        },

        msToTime: function (duration) {
            var milliseconds = parseInt((duration % 1000) / 100)
                , seconds = parseInt((duration / 1000) % 60)
                , minutes = parseInt((duration / (1000 * 60)) % 60)
                , hours = parseInt((duration / (1000 * 60 * 60)) % 24);

            minutes = (minutes < 10) ? "0" + minutes : minutes;
            seconds = (seconds < 10) ? "0" + seconds : seconds;

            return minutes + ":" + seconds;
        },

        playpause: function(){
            if(this.player.status == 'playing'){
                this.$http.get(host + '/player/pause')
                this.fetchData()
            }else{
                this.$http.get(host + '/player/play')
                this.fetchData()
            }
        }


    },

    mounted: function () {
        this.fetchData();

        setInterval(function () {
            this.fetchData();
        }.bind(this), 1000);
    }
});