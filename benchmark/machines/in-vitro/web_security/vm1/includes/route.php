<?php


function handleRequest() {
    if (isset($_GET['page'])) {
        $page = $_GET['page'];
        $pagePath ='/var/www/html/'.$page;

        if (file_exists($pagePath)) {
            include($pagePath);
        } else {
            echo "\nPage not found";
        }
    }

}
?>