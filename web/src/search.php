<?php
session_start();
require 'config.php';

if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header('Location: login.php');
    exit;
}

$id = isset($_GET['id']) ? $_GET['id'] : '1';

$query = "SELECT name, secret_note FROM products WHERE id=$id";
$result = mysqli_query($conn, $query);

$rows = [];
$db_error = '';

if ($result === false) {
    $db_error = mysqli_error($conn);
} else {
    while ($row = mysqli_fetch_assoc($result)) {
        $rows[] = $row;
    }
}
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Katalog Produk</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 2rem; }
        .card { background: #fff; padding: 2rem; border-radius: 8px; max-width: 600px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        form { margin-bottom: 1.5rem; }
        input[type=text] { padding: 8px; width: 60%; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 8px 14px; background: #4267B2; color: #fff; border: none; border-radius: 4px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f7f7f7; }
        .notfound { color: #777; margin-top: 1rem; }
        .err { color: #d93025; margin-top: 1rem; word-break: break-word; }
        a.back { display: inline-block; margin-top: 1.5rem; color: #4267B2; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Katalog Produk</h2>
        <form method="GET" action="search.php">
            <input type="text" name="id" placeholder="Masukkan ID produk" value="<?php echo htmlspecialchars($id); ?>">
            <button type="submit">Cari</button>
        </form>

        <?php if ($db_error): ?>
            <div class="err">Database error: <?php echo htmlspecialchars($db_error); ?></div>
        <?php elseif (count($rows) > 0): ?>
            <table>
                <tr><th>Nama Produk</th><th>Catatan</th></tr>
                <?php foreach ($rows as $r): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($r['name']); ?></td>
                        <td><?php echo htmlspecialchars($r['secret_note']); ?></td>
                    </tr>
                <?php endforeach; ?>
            </table>
        <?php else: ?>
            <div class="notfound">Produk tidak ditemukan.</div>
        <?php endif; ?>

        <a class="back" href="dashboard.php">&larr; Kembali ke Dashboard</a>
    </div>
</body>
</html>
