<?php
require __DIR__ . '/db.php';
try {
  $rows = db()->query('SELECT name, type, description AS `desc`, url, is_payment, tags FROM projects ORDER BY sort_order, id')->fetchAll();
  json_out(array_map(fn($r) => [
    'name' => $r['name'], 'type' => $r['type'], 'desc' => $r['desc'], 'url' => $r['url'],
    'pay'  => (int)$r['is_payment'],
    'tags' => array_values(array_filter(array_map('trim', explode(',', $r['tags'])))),
  ], $rows));
} catch (Throwable $e) {
  json_out(['error' => 'unavailable'], 503);
}
