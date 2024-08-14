import * as Tone from 'tone';

class AudioManager {
    tones = {
        "acoustic_grand_piano": "https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/acoustic_grand_piano-mp3/",
        "bright_acoustic_piano": "https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/bright_acoustic_piano-mp3/",
        "electric_grand_piano": "https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/electric_grand_piano-mp3/",
        "honkytonk_piano": "https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/honkytonk_piano-mp3/",

    };

    constructor() {
        this.sampler = null;
        this.gainNode = null;
        this.filterNode = null;
        this.setupAudio();
    }

    setupAudio() {
        this.url = this.tones.acoustic_grand_piano;
        // 使用正确的 Soundfont 音色库 URL
        this.sampler = new Tone.Sampler({
            urls: {
                "C3": "C3.mp3",
                "Db3": "Db3.mp3",
                "D3": "D3.mp3",
                "Eb3": "Eb3.mp3",
                "E3": "E3.mp3",
                "F3": "F3.mp3",
                "Gb3": "Gb3.mp3",
                "G3": "G3.mp3",
                "Ab3": "Ab3.mp3",
                "A3": "A3.mp3",
                "Bb3": "Bb3.mp3",
                "B3": "B3.mp3",

                "C4": "C4.mp3",
                "Db4": "Db4.mp3",
                "D4": "D4.mp3",
                "Eb4": "Eb4.mp3",
                "E4": "E4.mp3",
                "F4": "F4.mp3",
                "Gb4": "Gb4.mp3",
                "G4": "G4.mp3",
                "Ab4": "Ab4.mp3",
                "A4": "A4.mp3",
                "Bb4": "Bb4.mp3",
                "B4": "B4.mp3",
            },
            baseUrl: this.url,
            onload: () => {
                console.log("Sampler loaded successfully!");
            }
        }).toDestination();

        // 创建 Web Audio API 的 GainNode 和 FilterNode
        this.gainNode = Tone.context.createGain();
        this.filterNode = Tone.context.createBiquadFilter();

        // 将 GainNode 连接到 FilterNode，再连接到 Tone.js 的输出
        this.sampler.connect(this.gainNode).connect(this.filterNode).connect(Tone.Destination);

        // 设置初始音量和滤波器频率
        this.gainNode.gain.setValueAtTime(0.5, Tone.context.currentTime);
        this.filterNode.frequency.setValueAtTime(1000, Tone.context.currentTime);
    }

    playNote(note) {
        if (this.sampler) {
            this.sampler.triggerAttack(note);
        }
    }

    stopNote(note) {
        if (this.sampler) {
            this.sampler.triggerRelease(note);
        }
    }

    setVolume(volume) {
        if (this.gainNode) {
            this.gainNode.gain.setValueAtTime(volume, Tone.context.currentTime);
        }
    }

    setFilterFrequency(frequency) {
        if (this.filterNode) {
            this.filterNode.frequency.setValueAtTime(frequency, Tone.context.currentTime);
        }
    }
}

export default new AudioManager();