#!/usr/bin/env bash
in=/usr/share/alsa/alsa.conf

cp $in{,.bak-`date +%Y%m%d_%H%M%S`}
sed  -i '/^pcm\.rear/ s/^#*/#/' $in
sed  -i '/^pcm\.center_lfe/ s/^#*/#/' $in
sed  -i '/^pcm\.side/ s/^#*/#/' $in
sed  -i '/^pcm\.surround71/ s/^#*/#/' $in
sed  -i '/^pcm\.hdmi/ s/^#*/#/' $in
sed  -i '/^pcm\.modem/ s/^#*/#/' $in
sed  -i '/^pcm\.phoneline/ s/^#*/#/' $in