/*
===========================================================
Спільні компоненти (сервер + базова структура застосунку)
===========================================================
*/

const express = require("express");
const path = require("path");
const app = express();

app.use(express.json()); // обробка JSON
app.use(express.static(path.join(__dirname, "public"))); // React build

// --- Імітація БД (для навчальної роботи) ---
let users = [];
let posts = [];
let comments = [];
let friendships = [];
let gameState = {
    players: {},
    score: {}
};

/*
===========================================================
Завдання 1: Онлайн-гра (проста логіка клікер-гри)
===========================================================
Ідея: користувач натискає кнопку → сервер рахує очки
*/

// Реєстрація гравця
app.post("/api/game/register", (req, res) => {
    const { username } = req.body;
    if (!username) return res.status(400).send("No username");

    gameState.players[username] = true;
    gameState.score[username] = 0;

    res.send({ message: "Player registered", username });
});

// Отримати стан гри
app.get("/api/game/state", (req, res) => {
    res.send(gameState);
});

// Зробити хід (клік)
app.post("/api/game/click", (req, res) => {
    const { username } = req.body;

    if (!gameState.players[username]) {
        return res.status(400).send("Player not found");
    }

    gameState.score[username] += 1;
    res.send({ score: gameState.score[username] });
});

/*
===========================================================
Завдання 2: Пости, коментарі, дружба
===========================================================
*/

// --- Користувачі ---
app.post("/api/users", (req, res) => {
    const { username } = req.body;
    const user = { id: users.length + 1, username };
    users.push(user);
    res.send(user);
});

// --- Дружба ---
app.post("/api/friends/add", (req, res) => {
    const { userId, friendId } = req.body;

    friendships.push({ userId, friendId });
    friendships.push({ userId: friendId, friendId: userId }); 
    // компроміс: робимо двосторонній зв’язок, хоча в реальності це може бути запит/підтвердження

    res.send({ message: "Friend added" });
});

// Отримати друзів
app.get("/api/friends/:userId", (req, res) => {
    const userId = parseInt(req.params.userId);

    const friends = friendships
        .filter(f => f.userId === userId)
        .map(f => users.find(u => u.id === f.friendId));

    res.send(friends);
});

// --- Пости ---
app.post("/api/posts", (req, res) => {
    const { userId, content } = req.body;

    const post = {
        id: posts.length + 1,
        userId,
        content,
        date: new Date()
    };

    posts.push(post);
    res.send(post);
});

// Отримати всі пости
app.get("/api/posts", (req, res) => {
    res.send(posts);
});

// --- Коментарі ---
app.post("/api/comments", (req, res) => {
    const { postId, userId, text } = req.body;

    const comment = {
        id: comments.length + 1,
        postId,
        userId,
        text,
        date: new Date()
    };

    comments.push(comment);
    res.send(comment);
});

// Отримати коментарі до поста
app.get("/api/comments/:postId", (req, res) => {
    const postId = parseInt(req.params.postId);

    const postComments = comments.filter(c => c.postId === postId);
    res.send(postComments);
});

/*
===========================================================
Frontend (React) — базова інтеграція
===========================================================
Компроміс: методичка допускає різні варіанти фронтенду,
але за умовою використовується React → сервер лише API + статичні файли
*/

// fallback для SPA
app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

/*
===========================================================
Запуск серверу
===========================================================
*/

app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});