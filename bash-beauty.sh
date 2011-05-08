<<HEAD
 _                _           _                                   
| |              | |         | |                        _         
| |__  _____  ___| |___ _____| |__  _____ _____ _   _ _| |_ _   _ 
|  _ \(____ |/___)  _  (_____)  _ \| ___ (____ | | | (_   _) | | |
| |_) ) ___ |___ | | | |     | |_) ) ____/ ___ | |_| | | |_| |_| |
|____/\_____(___/|_| |_|     |____/|_____)_____|_____/ |___)\__  |
                                                           (____/ 

#################################################################
Name:           bash-beauty
Author:         Tim White
Company:        Zulius
Version:        0.0.1
Website:        http://www.zulius.com
Description:    Bash function library for displaying beautiful 
                script progress output.  
                The functions imitate the display format of 
                Linux boot messages. 
Example output:

    Executing command foo                        [  OK  ]
    Reading file /bar/baz                        [  OK  ]            
    Copying directory /bar                       [FAILED]

License:

    Copyright (C) 2009 Zulius

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#################################################################

HEAD

<<PRINTTASK
NAME
        printTask - utility function for printing columnar messages to terminal/log file

SYNOPSIS
        printTask [OPTION]... MESSAGE

OPTIONS:
        -t      flag to automatically prepend message with 14 digit timestamp
        -l      specify log file to write to
        -q      quiet mode. Do not output to stdout, only write to log file if supplied
        -w      width of padded message column. Defaults to 80 characters.

USAGE:
        1)  Print message to terminal:
        
              printTask "Gittin 'er done"

            OUTPUT to terminal:
            
              Gittin 'er done                                                                 

        2)  Print message to terminal and log file with prepended date stamp

              printTask -t -l "/tmp/foobar" "Gittin 'er done"

            OUTPUT to terminal:

              20091113085326  Gittin 'er done                                                  

            OUTPUT to log file:
              
              20091113085326  Gittin 'er done
        
PRINTTASK

printTask()
{
  _TP_THE_DATE=''
  _TP_LOG_PATH=''
  _TP_QUIET=''
  _TP_COLUMN_PAD=80

  # get options
  OPTIND=1
  while getopts ":tql:w:" OPT; do
    case $OPT in
      t) _TP_THE_DATE=$(date +"%Y%m%d%H%M%S  ") ;;
      q) _TP_QUIET=1 ;;
      l) _TP_LOG_PATH=$OPTARG ;;
      w) _TP_COLUMN_PAD=$OPTARG ;;
      :)
    esac
  done

  # get remaining arguments
  shift $(($OPTIND - 1))
  OPTIND=1

  _TP_COLUMN_PAD="%-${_TP_COLUMN_PAD}s"

  # quiet mode, print only to log file
  if [ ! -z "$_TP_QUIET" ] && [ ! -z "$_TP_LOG_PATH" ]; then
    printf "$_TP_COLUMN_PAD" "$_TP_THE_DATE${1}" >> "$_TP_LOG_PATH"
    return 0
  fi

  # non-quiet mode with log file
  if [ -z "$_TP_QUIET" ] && [ ! -z "$_TP_LOG_PATH" ]; then 
    printf "$_TP_COLUMN_PAD" "${_TP_THE_DATE}${1}" | tee -a "$_TP_LOG_PATH"
    return 0
  fi
  
  # no log file
  printf "$_TP_COLUMN_PAD" "${_TP_THE_DATE}${1}"

  return 0
}

<<PRINTOK
NAME
        printOk - utility function for printing green [  OK  ] to terminal/log file.
                  Meant to be used after printTask.

SYNOPSIS
        printOk [OPTION]...

OPTIONS:
        -l      specify log file to write to
        -q      quiet mode. Do not output to stdout, only write to log file if supplied

USAGE:
        1)  Print [  OK  ] to terminal:

              printTask "Gittin 'er done"
              printOk

            OUTPUT to terminal:

              Gittin 'er done                                                                 [  OK  ]

        2)  Print task message and [  OK  ] to terminal and log file with prepended date stamp
            with column width of 50:

              printTask -t -w 50 -l "/tmp/foobar" "Gittin 'er done"
              printOk -l "/tmp/foobar"

            OUTPUT to terminal:

              20091113090646  Gittin 'er done                   [  OK  ]

            OUTPUT to log file:

              20091113090646  Gittin 'er done                   [  OK  ]

PRINTOK

printOk()
{
  _TP_COLOR_RESET="\x1b[39;49;00m"
  _TP_COLOR_GREEN="\x1b[32;01m"
  _TP_OK="[  OK  ]" 

  _TP_LOG_PATH=''
  _TP_QUIET=''

  # get options
  OPTIND=1
  while getopts ":ql:" OPT; do
    case $OPT in
      q) _TP_QUIET=1 ;;
      l) _TP_LOG_PATH=$OPTARG ;;
      :)
    esac
  done
  
  # get remaining arguments
  shift $(($OPTIND - 1))
  OPTIND=1

  _tpStatusPrint 1 "" "$_TP_LOG_PATH" "$_TP_QUIET" 

  return 0
}

<<PRINTFAIL
NAME
        printFail - utility function for printing red [FAILED] to terminal/log file,
                    with optional failure message. Meant to be used after printTask.

SYNOPSIS
        printFail [OPTION]... [MESSAGE]

OPTIONS:
        -l      specify log file to write to
        -q      quiet mode. Do not output to stdout, only write to log file if supplied

USAGE:
        1)  Print [  FAIL  ] to terminal:

              printTask "Gittin 'er done"
              printFail

            OUTPUT to terminal:

              Gittin 'er done                                                                 [FAILED]

        2)  Print message, [FAILED], and failure message to terminal and log file with 
            prepended date stamp and column width of 50:

              printTask -t -w 50 -l "/tmp/foobar" "Gittin 'er done"
              printFail -l "/tmp/foobar" "Unable to git 'er done, beer consumption overflow error"

            OUTPUT to terminal:

              20091113090646  Gittin 'er done                   [FAILED]

              Unable to git 'er done, beer consumption overflow error

            OUTPUT to log file:

              20091113090646  Gittin 'er done                   [FAILED]

              Unable to git 'er done, beer consumption overflow error

PRINTFAIL


printFail()
{
  _TP_LOG_PATH=''
  _TP_QUIET=''

  # get options
  OPTIND=1
  while getopts ":ql:" OPT; do
    case $OPT in
      q) _TP_QUIET=1 ;;
      l) _TP_LOG_PATH=$OPTARG ;;
      :)
    esac
  done

  # get remaining arguments
  shift $(($OPTIND - 1))
  OPTIND=1

  _tpStatusPrint 2 "$1" "$_TP_LOG_PATH" "$_TP_QUIET"

  return 0

}

<<PRINTWARN
NAME
        printWarn - utility function for printing yellow [ WARN ] to terminal/log file.
                    Meant to be used after printTask.

SYNOPSIS
        printWarn [OPTION]...

OPTIONS:
        -l      specify log file to write to
        -q      quiet mode. Do not output to stdout, only write to log file if supplied

USAGE:
        1)  Print [ WARN ] to terminal:

              printTask "Gittin 'er done"
              printWarn

            OUTPUT to terminal:

              Gittin 'er done                                                                 [ WARN ]

        2)  Print task message and [ WARN ] to terminal and log file with prepended date stamp
            with column width of 50:

              printTask -t -w 50 -l "/tmp/foobar" "Gittin 'er done"
              printWarn -l "/tmp/foobar"

            OUTPUT to terminal:

              20091113090646  Gittin 'er done                   [ WARN ]

            OUTPUT to log file:

              20091113090646  Gittin 'er done                   [ WARN ]

PRINTWARN

printWarn()
{
  _TP_LOG_PATH=''
  _TP_QUIET=''

  # get options
  OPTIND=1
  while getopts ":ql:" OPT; do
    case $OPT in
      q) _TP_QUIET=1 ;;
      l) _TP_LOG_PATH=$OPTARG ;;
      :)
    esac
  done
  
  # get remaining arguments
  shift $(($OPTIND - 1))
  OPTIND=1

  _tpStatusPrint 3 "" "$_TP_LOG_PATH" "$_TP_QUIET" 

  return 0
}

<<PRINTINFO
NAME
        printInfo - utility function for printing blue [ INFO ] to terminal/log file.
                    Meant to be used after printTask.

SYNOPSIS
        printInfo [OPTION]...

OPTIONS:
        -l      specify log file to write to
        -q      quiet mode. Do not output to stdout, only write to log file if supplied

USAGE:
        1)  Print [ INFO ] to terminal:

              printTask "Gittin 'er done"
              printInfo

            OUTPUT to terminal:

              Gittin 'er done                                                                 [ INFO ]

        2)  Print task message and [ INFO ] to terminal and log file with prepended date stamp
            with column width of 50:

              printTask -t -w 50 -l "/tmp/foobar" "Gittin 'er done"
              printInfo -l "/tmp/foobar"

            OUTPUT to terminal:

              20091113090646  Gittin 'er done                   [ INFO ]

            OUTPUT to log file:

              20091113090646  Gittin 'er done                   [ INFO ]

PRINTINFO

printInfo()
{
  _TP_LOG_PATH=''
  _TP_QUIET=''

  # get options
  OPTIND=1
  while getopts ":ql:" OPT; do
    case $OPT in
      q) _TP_QUIET=1 ;;
      l) _TP_LOG_PATH=$OPTARG ;;
      :)
    esac
  done
  
  # get remaining arguments
  shift $(($OPTIND - 1))
  OPTIND=1

  _tpStatusPrint 4 "" "$_TP_LOG_PATH" "$_TP_QUIET" 

  return 0
}


<<_TPSTATUSPRINT
  Private method, not really meant for usage outside this script.

  $1  integer     status
  $2  string      message
  $3  string      log file path
  $4  integer     quiet mode

_TPSTATUSPRINT

_tpStatusPrint(){
  _TP_COLOR_RESET="\x1b[39;49;00m"

  _TP_STATUS=''
  _TP_COLOR=''

  case $1 in
      1) _TP_STATUS="[  OK  ]"; _TP_COLOR="\x1b[33;32m";;
      2) _TP_STATUS="[FAILED]"; _TP_COLOR="\x1b[31;31m";;
      3) _TP_STATUS="[ WARN ]"; _TP_COLOR="\x1b[33;33m";;
      4) _TP_STATUS="[ INFO ]"; _TP_COLOR="\x1b[36;01m";;
      *) _TP_STATUS="[ ???? ]"; _TP_COLOR="";;
  esac

  # quiet mode, print only to log file
  if [ ! -z "$4" ] && [ ! -z "$3" ]; then
    echo -e "$_TP_STATUS" >> $3

    # supplementary message
    if [ ! -z "$2" ]; then
      echo -e "\n$2\n" >> "$3"
    fi
    return 0
  fi

  # non-quiet mode with log file
  if [ -z "$4" ] && [ ! -z "$3" ]; then
    echo -e "${_TP_COLOR}${_TP_STATUS}${_TP_COLOR_RESET}"
    echo -e "${_TP_STATUS}" >> "$3"

    # supplementary message
    if [ ! -z "$2" ]; then
      echo -e "\n${_TP_COLOR}${2}${_TP_COLOR_RESET}\n"
      echo -e "\n$2\n" >> "$3"
    fi

    return 0
  fi

  echo -e "${_TP_COLOR}${_TP_STATUS}${_TP_COLOR_RESET}"

  # supplementary message
  if [ ! -z "$2" ]; then
    echo -e "\n${_TP_COLOR}${2}${_TP_COLOR_RESET}\n"
  fi
  return 0
}
