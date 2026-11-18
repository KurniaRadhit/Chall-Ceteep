<?php

$db_host = getenv('DB_HOST') ?: 'db';
$db_user = getenv('DB_USER') ?: 'Storeapp01';
$db_pass = getenv('DB_PASS') ?: 'Kj7mPz2qXr';
$db_name = getenv('DB_NAME') ?: 'Shopdb10';

$conn = mysqli_connect($db_host, $db_user, $db_pass, $db_name);

if (!$conn) {
    die("Koneksi database gagal: " . mysqli_connect_error());
}
?>
