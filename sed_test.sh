#!/bin/sh

T1="tv/game.of.thrones/s1/game.of.thrones.s01e03.lord.snow.hdtv.xvid-fqm.avi"
T2="tv/the.office.us/ tv/the.office.us/s7/ tv/the.office.us/s7/the.office.us.s07e22.hdtv.xvid-fqm.avi"
T3="tv/the.office/s5/the.office.us.s05e20.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e21.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e22.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e23.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e24.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e25.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e26.dvdrip.xvid-reward.avi"
T4="tv/the.office/s5/the.office.us.s05e18.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e19.dvdrip.xvid-reward.avi tv/the.office/s5/the.office.us.s05e20. rsync: writefd_unbuffered failed to write 4 bytes to socket [sender]: Broken pipe (32) rsync: connection unexpectedly closed (87 bytes received so far) [sender] rsync error: error in rsync protocol data stream (code 12) at io.c(601) [sender=3.0.7]"

# echo $T1 | sed s_tv/.*/__
# echo $T1 | sed 's/ /\n/g' | sed s_tv/.*/__
# echo $T2 | sed 's/ /\n/g' | sed s_tv/.*/__
# echo $T3 | sed 's/ /\n/g' | sed s_tv/.*/__
# echo $T4 | sed 's/ /\n/g' | sed s_tv/.*/__

# echo $T1 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed s_tv/.*/__ | sed '/^$/d' 
# echo $T2 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed s_tv/.*/__ | sed '/^$/d' 
# echo $T3 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed s_tv/.*/__ | sed '/^$/d' 
# echo $T4 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed s_tv/.*/__ | sed '/^$/d' 


T5="i.love.you.phillip.morris/ukd-ilypm.avi i.love.you.phillip.morris/ukd-ilypm.nfo la.confidential/l.a.-confidential[1997]dvdrip[eng]-zeus.dias.avi monsters/FXG\#303\#242\#302\#204\#302\#242.nfo monsters/Monsters[2010]DvDrip[Eng]-FXG.avi monsters/Monsters[Eng][Subs].srt monsters/Torrent downloaded from extratorrent.com.txt no.strings.attached/No Strings Attached (2011) DvDRiP Eng-BULLDOZER.rar pay.it.forward/CPtScene-pif-xvid.avi pay.it.forward/Pay.It.Forward.2000.DVDRip.XviD-CPtScene.nfo pay.it.forward/shots/CPtScene-pif-xvid1.jpg pay.it.forward/shots/CPtScene-pif-xvid2.jpg pay.it.forward/shots/CPtScene-pif-xvid3.jpg pay.it.forward/shots/CPtScene-pif-xvid4.jpg pay.it.forward/subs/CPtScene-pif-xvid-en.srt pay.it.forward/subs/CPtScene-pif-xvid-es.srt pay.it.forward/subs/CPtScene-pif-xvid-ptbr.srt scott.pilgrim.vs.the.world/FXG\#342\#204\#242.nfo scott.pilgrim.vs.the.world/Scott Pilgrim vs. the World[2010]DvDrip[Eng]-FXG.avi scott.pilgrim.vs.the.world/Scott Pilgrim vs. the World[2010]DvDrip[Eng]-FXG.txt scott.pilgrim.vs.the.world/Scott Pilgrim vs. the World[Eng][Subs].srt swimming.with.sharks/Swimming with Sharks (1994) DVDRip WS XviD.avi swimming.with.sharks/Torrent downloaded from Demonoid.com.txt the.double.hour/The Double Hour (2011) DvDRiP Eng-SURViVAL.rar the.fighter/The Fighter (2010) DVDRip XviD-MAXSPEED www.torentz.3xforum.ro.avi the.fighter/The Fighter (2010) DVDRip XviD-MAXSPEED.nfo the.fighter/Torrent downloaded from Demonoid.me.txt the.fighter/Torrent downloaded from Extratorrent.com.txt the.fighter/Torrent downloaded from Rarbg.com.txt the.fighter/Torrent downloaded from h33t.com.txt the.fighter/sample.avi the.fighter/screencaps.jpg the.green.hornet/Sample.avi the.green.hornet/The.Green.Hornet.2010.TS.XViD-T0XiC-iNK.avi W rsync: writefd_unbuffered failed to write 4 bytes to socket [sender]: No child processes (10) rsync: connection unexpectedly closed (666 bytes received so far) [sender] rsync error: unexplained error (code 255) at io.c(601) [sender=3.0.7]"

T6=" rsync: connection unexpectedly closed (0 bytes received so far) [sender] rsync error: unexplained error (code 255) at io.c(601) [sender=3.0.7]"

# echo $T6 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed s_tv/.*/__ | sed '/^$/d' 
echo $T5 | sed 's/rsync:.*]//' | sed 's/ /\n/g' | sed 's/\(.*[\/]\).*/\1/' | grep "/$" | sed '/^$/d' 



# | sed s_tv/.*/__
# echo $T3 | sed s_tv/.*/__
# echo $T4 | sed s_tv/.*/__
# echo $T1 | grep [tv/[.*]/s[0-9]*]
