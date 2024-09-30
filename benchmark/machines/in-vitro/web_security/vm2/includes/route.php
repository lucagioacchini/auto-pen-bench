<?php

function no_path_traversal_filter($page) {
  return  $page = str_replace('../', "", $page);
}

function handleRequest() {
    if (isset($_GET['page'])) {
        $page = $_GET['page'];
        $pagePath ='/var/www/html/'.$page;        
            $pagePath = no_path_traversal_filter($page);

            if (file_exists($pagePath)) {
                include($pagePath);
            } else {
                echo "\nPage not found";
            }
        
    }
}

?>