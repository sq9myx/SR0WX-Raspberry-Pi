<?php

$data = file_get_contents('https://www.gismeteo.pl/weather-zywiec-3059/gm/');

file_put_contents('gisMeteo.html', $data);

echo $data;
