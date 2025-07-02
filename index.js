const axios = require("axios");
const https = require("https");
const express = require("express");
const fetch = require("node-fetch");
const { performance } = require("perf_hooks");
const app = express();

const email = "123456789xdf3@gmail.com";
const password = "Gehrman3mk";
const commentText = "    ";

// ✅ سرعة الإرسال: 60 تعليق بالدقيقة = 1 تعليق كل ثانية لكل أنمي
const delayPerAnime = 1000;

// ✅ عدد التعليقات المراد إرسالها لكل أنمي
const maxCommentsPerAnime = 60;

const animeTargets = {
  532: true, 11708: true, 11547: true, 11707: true, 11723: true, 11706: true,
  11673: true, 11704: true, 11703: true, 11702: true, 11700: true, 11705: true,
  11699: true, 11698: true, 11694: true, 11697: true, 11721: true, 11718: true,
  11693: true, 11692: true, 11663: true, 11710: true, 11711: true, 11691: true,
  11689: true, 653: true, 11686: true, 11688: true, 11684: true, 11712: true,
  11715: true, 11658: true, 11725: true, 11726: true,
};

const headers = {
  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X)",
  "Content-Type": "application/x-www-form-urlencoded",
  "Origin": "https://ios.sanime.net",
  "Referer": "https://ios.sanime.net/",
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate, br",
  "Connection": "keep-alive",
  "Accept-Language": "ar"
};

const agent = new https.Agent({ keepAlive: true });
let botActive = true;
let totalCommentsSent = 0;
const animeProgress = {}; // تتبع عدد التعليقات لكل أنمي

// دالة إرسال تعليق
async function sendComment(animeId) {
  const itemData = {
    post: commentText,
    id: animeId,
    fire: false
  };

  const itemBase64 = Buffer.from(JSON.stringify(itemData)).toString("base64");
  const payload = new URLSearchParams({
    email,
    password,
    item: itemBase64
  });

  try {
    await axios.post(
      "https://app.sanime.net/function/h10.php?page=addcmd",
      payload.toString(),
      {
        headers,
        httpsAgent: agent,
        timeout: 7000
      }
    );
    totalCommentsSent++;
    animeProgress[animeId] = (animeProgress[animeId] || 0) + 1;
    console.log(`✅ [${animeId}] تعليق رقم ${animeProgress[animeId]}`);
  } catch (err) {
    console.error(`❌ [${animeId}] خطأ: ${err.message}`);
  }
}

// توزيع إرسال التعليقات عبر الزمن
function startSmartDispatcher() {
  const activeAnimeIds = Object.keys(animeTargets).filter(id => animeTargets[id]);

  activeAnimeIds.forEach((animeId, index) => {
    animeProgress[animeId] = 0;

    setTimeout(() => {
      setInterval(() => {
        if (!botActive) return;
        if (animeProgress[animeId] >= maxCommentsPerAnime) return;
        sendComment(animeId);
      }, delayPerAnime);
    }, index * (delayPerAnime / activeAnimeIds.length)); // توزيع الحمل
  });
}

// 🟢 حالة البوت
app.get("/", (req, res) => {
  res.send(`
    🤖 Bot is running...<br>
    📊 التعليقات المرسلة: ${totalCommentsSent}<br>
    💡 سرعة: 60 تعليق/د لكل أنمي<br>
    🧩 عدد الأنميات: ${Object.keys(animeTargets).length}
  `);
});

// 🔘 إيقاف
app.get("/stop", (req, res) => {
  botActive = false;
  res.send("🛑 تم إيقاف البوت مؤقتًا");
});

// 🔘 تشغيل
app.get("/start", (req, res) => {
  botActive = true;
  res.send("✅ تم تشغيل البوت");
});

// 🔁 إبقاء الخدمة حية
const KEEP_ALIVE_URL = "https://auto-comment-bot-rrmb.onrender.com/";
setInterval(() => {
  fetch(KEEP_ALIVE_URL)
    .then(() => console.log("🔁 Keep-alive ping sent"))
    .catch(err => console.error("⚠️ Keep-alive ping failed:", err.message));
}, 5 * 60 * 1000);

// 🚀 بدء البوت
startSmartDispatcher();

// 🖥️ بدء السيرفر
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log(`🌐 Web server running on port ${PORT}`);
});
