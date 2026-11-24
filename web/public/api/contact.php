<?php
require __DIR__ . '/db.php';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_out(['ok' => false, 'error' => 'POST only'], 405);
$in = json_decode(file_get_contents('php://input'), true) ?: $_POST;
if (!empty($in['website'])) json_out(['ok' => true]);            // honeypot: bots see "success"
$name  = trim((string)($in['name'] ?? ''));
$email = trim((string)($in['email'] ?? ''));
$msg   = trim((string)($in['message'] ?? ''));
if (mb_strlen($name) < 2 || mb_strlen($name) > 80 || !filter_var($email, FILTER_VALIDATE_EMAIL)
    || mb_strlen($msg) < 5 || mb_strlen($msg) > 2000) {
  json_out(['ok' => false, 'error' => 'Please check your details.'], 422);
}
$ip = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . (getenv('APP_SECRET') ?: 'change-me'));
try {
  $pdo = db();
  $c = $pdo->prepare('SELECT COUNT(*) FROM messages WHERE ip_hash = ? AND created_at > NOW() - INTERVAL 10 MINUTE');
  $c->execute([$ip]);
  if ((int)$c->fetchColumn() >= 3) json_out(['ok' => false, 'error' => 'Too many messages. Try again later.'], 429);
  $pdo->prepare('INSERT INTO messages (name, email, message, ip_hash) VALUES (?, ?, ?, ?)')->execute([$name, $email, $msg, $ip]);
  json_out(['ok' => true]);
} catch (Throwable $e) {
  json_out(['ok' => false, 'error' => 'Server error'], 500);
}
