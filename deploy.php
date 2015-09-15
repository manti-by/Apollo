<?php

define('LOCAL_ROOT', dirname(__FILE__));
define('REMOTE_ROOT', '/home/pi/pibot/');

$connection = ssh2_connect('192.168.1.10', 22);
ssh2_auth_password($connection, 'pi', 'raspberry');

clearstatcache();
$iterator = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator(LOCAL_ROOT, RecursiveDirectoryIterator::SKIP_DOTS)
);
foreach ($iterator as $item) {
    if ($item->isFile()) {
        $local_path = $item->getRealPath();
        $remote_path = str_replace(LOCAL_ROOT, REMOTE_ROOT, $path);
        
        try {
            ssh2_scp_send($connection, $local_path, $remote_path, 0644);
            echo '[OK] ' . $path . ' - deployed succesfully';
        } catch (Exception $e) {
            echo '[ERROR] ' . $path . ' - ' . $e->getMessage();
        }
    }
}
