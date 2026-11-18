<?php
session_start();
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header('Location: login.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 2rem; }
        .card { background: #fff; padding: 2rem; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { color: #333; }
        a.btn { display: inline-block; margin-top: 1rem; padding: 10px 16px; background: #4267B2; color: #fff; text-decoration: none; border-radius: 4px; }
        a.logout { margin-left: 10px; color: #d93025; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Selamat datang, <?php echo htmlspecialchars($_SESSION['username']); ?>!</h2>
        <p>Anda berhasil login ke sistem.</p>
        <p>Gunakan fitur pencarian produk di bawah ini untuk melihat katalog kami.</p>
        <a class="btn" href="search.php?id=1">Buka Pencarian Produk</a>
        <a class="logout" href="logout.php">Logout</a>
    </div>
</body>
</html>
