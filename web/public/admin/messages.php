<?php
require __DIR__ . '/../api/db.php';
$pw = getenv('ADMIN_PASSWORD');
if (!$pw) { http_response_code(503); exit('Set ADMIN_PASSWORD in .env to enable this page.'); }
if (!isset($_SERVER['PHP_AUTH_PW']) || !hash_equals($pw, $_SERVER['PHP_AUTH_PW'])) {
  header('WWW-Authenticate: Basic realm="Admin"'); http_response_code(401); exit('Login required');
}
header('X-Robots-Tag: noindex');
$rows = db()->query('SELECT name, email, message, created_at FROM messages ORDER BY id DESC LIMIT 100')->fetchAll();
$e = fn($s) => htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
?><!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Messages</title>
<style>body{font:16px system-ui;max-width:800px;margin:40px auto;padding:0 16px;background:#F2FAFD;color:#0B1F3A}article{background:#fff;border:2px solid #0B1F3A;border-radius:14px;padding:16px;margin:14px 0}small{color:#46607F}</style>
<h1>Messages (<?= count($rows) ?>)</h1>
<?php foreach ($rows as $r): ?><article><b><?= $e($r['name']) ?></b> · <a href="mailto:<?= $e($r['email']) ?>"><?= $e($r['email']) ?></a> <small><?= $e($r['created_at']) ?></small><p><?= nl2br($e($r['message'])) ?></p></article><?php endforeach; ?>
