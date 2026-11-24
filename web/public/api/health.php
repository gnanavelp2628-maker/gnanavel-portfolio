<?php
require __DIR__ . '/db.php';
$h = ['php' => PHP_VERSION, 'db' => ['ok' => false], 'ai' => ['ok' => false]];
try {
  $p = db();
  $h['db'] = ['ok' => true, 'version' => $p->query('SELECT VERSION()')->fetchColumn(),
              'projects' => (int)$p->query('SELECT COUNT(*) FROM projects')->fetchColumn()];
} catch (Throwable $e) {}
$ctx = stream_context_create(['http' => ['timeout' => 2]]);
$h['ai']['ok'] = @file_get_contents('http://chatbot:8000/', false, $ctx) !== false;
json_out($h);
