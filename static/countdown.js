
const countdownBox = document.getElementById('countdown-box')

const now = new Date().getTime()
const nextDay = new Date(now);
nextDay.setDate(nextDay.getDate() + 1);
nextDay.setHours(12, 0, 0, 0);
const diff = nextDay - new Date();
setInterval(()=>{
    const now = new Date().getTime()
    const diff = nextDay - now
    const d = Math.floor(nextDay / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const h = Math.floor((nextDay / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const m = Math.floor((nextDay / (1000 * 60) - (now / (1000 * 60))) % 60)
    const s = Math.floor((nextDay / (1000) - (now / (1000))) % 60)

    if (diff > 0) {
        countdownBox.innerHTML = h + 'h:' + ('0' + m).slice(-2) + 'm:' + ('0' + s).slice(-2) + 's';
    } else {
        nextDay.setDate(nextDay.getDate() + 1);
        nextDay.setHours(12, 0, 0, 0);
    }
},1000)









