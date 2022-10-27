FSI XML

Here is a zone sensing fault example, starting with a 500 series APU zone going into fault. 
Note that this is reported by having the DeviceState change to the Fault state.
다음은 결함이있는 500 시리즈 APU 영역으로 시작하는 영역 감지 결함 예입니다.
이는 DeviceState를 Fault 상태로 변경하여보고됩니다.

    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceDetectionReport>
        <DeviceDetectionRecord>
            <DeviceIdentification>
                <DeviceName>FD508-100913.HZONE-2.ZONE-006</DeviceName>
                <DeviceCategory>Sensor</DeviceCategory>
                <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Detection>
                <ID>SZ00015</ID>
                <DetectionEvent>Fault</DetectionEvent>
                <UpdateTime Zone="GMT">2070-01-03T08:13:49.164</UpdateTime>
            </Detection>
        </DeviceDetectionRecord>
    </DeviceDetectionReport>

    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceStatusReport>
        <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-2.ZONE-006</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
        </DeviceIdentification>
        <Status>
            <DeviceState>Fault</DeviceState>
            <CommunicationState>Fail</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:13:49.165</UpdateTime>
        </Status>
    </DeviceStatusReport>



When the zone comes out of fault, the DeviceState changes to the Secure state :
영역에 오류가 발생하면 DeviceState가 보안 상태로 변경됩니다.
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceStatusReport>
        <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-2.ZONE-006</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
        </DeviceIdentification>
        <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:13:58.161</UpdateTime>
        </Status>
        <Detection>
            <DetectionEvent>Other</DetectionEvent>
            <Details>Internal line fault</Details>
            <UpdateTime Zone="GMT">2070-01-03T08:13:58.161</UpdateTime>
        </Detection>
    </DeviceStatusReport>




Example message to APU -- unknown APU:
    <CommandMessage MessageType="Request">
        <DeviceIdentification>
            <DeviceName></DeviceName>
        </DeviceIdentification>
        <Command>
            <SimpleCommand>Ping</SimpleCommand>
        </Command>
    </CommandMessage>


Example response from APU to request with unknown APU:
    <?xml version="1.0" encoding="UTF-8"?>
    <CommandMessage MessageType="Response" Status="Failed">
        <DeviceIdentification>
            <DeviceName>E102332</DeviceName>
        </DeviceIdentification>
        <Command>
            <SimpleCommand>Ping</SimpleCommand>
        </Command>
    </CommandMessage>


Example message to APU -- known APU:
    <CommandMessage MessageType="Request">
        <DeviceIdentification>
            <DeviceName>E102332</DeviceName>
        </DeviceIdentification>
        <Command>
            <SimpleCommand>Ping</SimpleCommand>
        </Command>
    </CommandMessage>


Example response from APU to request with known APU:
    <?xml version="1.0" encoding="UTF-8"?>
    <CommandMessage MessageType="Response" Status="OK">
        <DeviceIdentification>
            <DeviceName>E102332</DeviceName>
        </DeviceIdentification>
        <Command>
            <SimpleCommand>Ping</SimpleCommand>
        </Command>
    </CommandMessage>


Example message from APU when a tamper condition occurs:
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceStatusReport>
        <DeviceIdentification>
        <DeviceName>E102419</DeviceName>
        <DeviceCategory>Sensor</DeviceCategory>
        <DeviceType>FD34x APU</DeviceType>
        </DeviceIdentification>
        <Status>
        <DeviceState>Tamper</DeviceState>
        <DeviceSubState>Open</DeviceSubState>
        <CommunicationState>OK</CommunicationState>
        <UpdateTime Zone="GMT">2014-05-07T14:53:27.000</UpdateTime>
        </Status>
        <Detection>
        <DetectionEvent>Tamper</DetectionEvent>
        <UpdateTime Zone="GMT">2014-05-07T14:53:27.000</UpdateTime>
        </Detection>
    </DeviceStatusReport>
 

Example message from APU when the tamper condition is resolved:
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceStatusReport>
        <DeviceIdentification>
        <DeviceName>E102419</DeviceName>
        <DeviceCategory>Sensor</DeviceCategory>
        <DeviceType>FD34x APU</DeviceType>
        </DeviceIdentification>
        <Status>
        <DeviceState>Secure</DeviceState>
        <CommunicationState>OK</CommunicationState>
        <UpdateTime Zone="GMT">2014-05-07T14:53:27.000</UpdateTime>
        </Status>
    </DeviceStatusReport>


Example message from APU when a zone has a sensing fault:
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceStatusReport>
        <DeviceIdentification>
        <DeviceName>APUNAME.CHB</DeviceName>
        <DeviceCategory>Sensor</DeviceCategory>
        <DeviceType>FD34x Channel</DeviceType>
        </DeviceIdentification>
        <Status>
        <DeviceState>Fault</DeviceState>
        <CommunicationState>Fail</CommunicationState>
        <UpdateTime Zone="GMT">2016-03-10T15:40:28.000</UpdateTime>
        </Status>
    </DeviceStatusReport>

Note that a DeviceDetectionReport will also be sent.


Example message from APU when the zone's sensing fault has been resolved:
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceStatusReport>
        <DeviceIdentification>
        <DeviceName>APUNAME.CHB</DeviceName>
        <DeviceCategory>Sensor</DeviceCategory>
        <DeviceType>FD34x Channel</DeviceType>
        </DeviceIdentification>
        <Status>
        <DeviceState>Secure</DeviceState>
        <CommunicationState>OK</CommunicationState>
        <UpdateTime Zone="GMT">2016-03-10T15:40:28.000</UpdateTime>
        </Status>
        <Detection>
        <DetectionEvent>Other</DetectionEvent>
        <Details>Internal line fault</Details>
        <UpdateTime Zone="GMT">2016-03-10T15:40:28.000</UpdateTime>
        </Detection>
    </DeviceStatusReport>

Note that a DeviceDetectionReport will NOT also be sent.


Additonal note:

Note that APUs shipping before 2014 differ slightly for the tamper messages. 
These APUs do not indicate when a tamper condition has been resolved. 
These APUs also do not include the "Open" DeviceSubState with the initial "Tamper" message. 
2014 년 이전에 배송되는 APU는 변조 메시지에 대해 약간 다릅니다.
이러한 APU는 변조 조건이 해결 된시기를 나타내지 않습니다.
이러한 APU에는 초기 "Tamper"메시지와 함께 "Open"DeviceSubState도 포함되지 않습니다.

So when a StatusType looks like this, it is from an older APU:
따라서 StatusType이 다음과 같으면 이전 APU에서 가져온 것입니다.
<DeviceState>Tamper</DeviceState>
<CommunicationState>OK</CommunicationState>

This means that the tamper condition will never be reported as resolved. 
So to best handle this, treat the tamper as it were a one-time event (similar to an Intrusion Alarm) rather than an on/off state value.
This technique is not neccessary to support APUs sold in 2014 or later.
이는 변조 조건이 해결 된 것으로보고되지 않음을 의미합니다.
따라서이를 가장 잘 처리하려면 탬퍼를 켜짐 / 꺼짐 상태 값이 아닌 일회성 이벤트 (침입 경보와 유사)로 취급하십시오.
이 기술은 2014 년 이후에 판매 된 APU를 지원하는 데 필요하지 않습니다.


DeviceNames are the fundamental way in which APUs and zones are identified. 
Full device names are hierarchical and use a period ('.') as a separator. 
Generally speaking, monitoring equipment should not need to parse the device name, just match the name up to previously identified names.
DeviceNames는 APU 및 영역을 식별하는 기본 방법입니다.
전체 장치 이름은 계층 적이며 마침표 ( '.')를 구분 기호로 사용합니다.
일반적으로 모니터링 장비는 장치 이름을 구문 분석 할 필요가 없으며 이름을 이전에 식별 된 이름과 일치시키기 만하면됩니다.

However, to understand how names are constructed, you must first understand the conceptual structure within APUs. 
There are differences between 300 series and 500 series APUs.
그러나 이름이 어떻게 구성되는지 이해하려면 먼저 APU 내의 개념적 구조를 이해해야합니다.
300 시리즈와 500 시리즈 APU에는 차이가 있습니다.

300 series is simpler, so we begin there. 300 series APUs have either one or two zones, depending on the model. 
The full name of the zone is "apu.zone", where "apu" is the name of the APU and "zone" is the partial name of the zone.
300 시리즈는 더 간단하므로 여기서 시작합니다. 300 시리즈 APU에는 모델에 따라 하나 또는 두 개의 영역이 있습니다.
영역의 전체 이름은 "apu.zone"입니다. 여기서 "apu"는 APU의 이름이고 "zone"은 영역의 부분 이름입니다.


By default, the APU has a name equal "E" plus the serial number.  
By default, the partial name of the first zone is "CHA" and the second zone is "CHB". 
The APU name and the partial zone names are settable using the APU configuration software.
기본적으로 APU의 이름은 "E"에 일련 번호를 더한 것과 같습니다.
기본적으로 첫 번째 영역의 부분 이름은 "CHA"이고 두 번째 영역은 "CHB"입니다.
APU 이름 및 부분 영역 이름은 APU 구성 소프트웨어를 사용하여 설정할 수 있습니다.

Some example 300 series names: 
"E100213" (an APU), 
"E100213.CHA" (a zone), 
"FOO" (an APU), and "FOO.BAR", (a zone).
300 시리즈 이름의 예 : 
"E100213"(APU), 
"E100213.CHA"(영역),
"FOO"(APU) 및 "FOO.BAR", (영역)

500 series APUs are similiar but contain an intermediate layer known as a "hyperzone". 
The APU contains hyperzones which contains zones. 
The hyperzones are groupings used for configuration purposes. 
500 시리즈 APU는 유사하지만 "하이퍼 존"이라는 중간 계층을 포함합니다.
APU에는 영역이 포함 된 하이퍼 존이 포함되어 있습니다.
하이퍼 존은 구성 목적으로 사용되는 그룹입니다.

Each zone must be located within a hyperzone and a hyperzone will only exist if it contains a zone. 
So the full name of a zone will be "apuname.hyperzone.zone", where "hyperzone" is the name of the hyperzone and "zone" is the partial name of the zone.
각 영역은 하이퍼 존 내에 있어야하며 하이퍼 존은 영역이 포함 된 경우에만 존재합니다.
따라서 영역의 전체 이름은 "apuname.hyperzone.zone"이됩니다. 여기서 "hyperzone"은 하이퍼 존의 이름이고 "zone"은 영역의 일부 이름입니다.

By default, the APU has a name equal to "model-serial", where "model" is the model name and "serial" is the serial number. 
Hyperzones have partial names "HZONE-#", where "#" is the number of the hyperzone. 
Users cannot change hyperzone names. 
By default, partial zone names have the form "ZONE-###", where "###" is the 3-digit number of the zone. 
기본적으로 APU의 이름은 "model-serial"과 동일합니다. 여기서 "model"은 모델 이름이고 "serial"은 일련 번호입니다.
하이퍼 존은 부분 이름 "HZONE- #"을 가지며, 여기서 "#"은 하이퍼 존의 번호입니다.
사용자는 하이퍼 존 이름을 변경할 수 없습니다.
기본적으로 부분 영역 이름의 형식은 "ZONE-###"이며, 여기서 "###"은 영역의 3 자리 숫자입니다.

The APU name and the partial zone names are settable using the APU configuration software. 
The hyperzone partial names cannot be changed, although the arrangement of which hyperzones contain which zones can also be set using the APU configuration software. 
By default, all zones are in the first hyperzone.
APU 이름 및 부분 영역 이름은 APU 구성 소프트웨어를 사용하여 설정할 수 있습니다.
하이퍼 존 부분 이름은 변경할 수 없지만, 하이퍼 존에 포함되는 배열은 APU 구성 소프트웨어를 사용하여 설정할 수도 있습니다.
기본적으로 모든 영역은 첫 번째 하이퍼 영역에 있습니다.

Some example 500 series names: 
"FD508-100213" (an APU), 
"FD508-100213.HZONE-3" (a hyperzone), 
"FD508-100213.HZONE-3.ZONE-012" (a zone), 
"FOO" (an APU), 
"FOO.HZONE-1", (a hyperzone), 
"FOO.HZONE-1.BAZ" (a zone).

WARNING: because the APU names can be changed, it is not appropriate to parse these names in an attempt to determine the model number and / or serial number of the device.

DeviceTypes are defined as follows. Generally speaking, the monitoring equipment does not need to use this information.
경고 : APU 이름은 변경 될 수 있으므로 장치의 모델 번호 및 / 또는 일련 번호를 확인하기 위해 이러한 이름을 구문 분석하는 것은 적절하지 않습니다.

DeviceType은 다음과 같이 정의됩니다. 일반적으로 모니터링 장비는이 정보를 사용할 필요가 없습니다.

300 series APU: "FD34x APU"
300 series zone: "FD34x Channel"
500 series APU: "SPIDR APU"
500 series hyperzone: "SPIDR Hyperzone"
500 series zone: "SPIDR Zone"


-------------------------------------


The PlatformStatusReport message is used to describe the hierarchical structure of the APU and its zones. 
There are differences between 300 series and 500 series APUs.
PlatformStatusReport 메시지는 APU 및 해당 영역의 계층 구조를 설명하는 데 사용됩니다.
300 시리즈와 500 시리즈 APU에는 차이가 있습니다.

300 series APUs contain zones directly and have either one or two zones. 
A PlatformStatusReport will be sent for the APU containing a DeviceStatusReport structure for each zone.
300 시리즈 APU는 영역을 직접 포함하고 하나 또는 두 개의 영역을 갖습니다.
각 영역에 대한 DeviceStatusReport 구조를 포함하는 APU에 대해 PlatformStatusReport가 전송됩니다.

500 series APUs are similiar but contain an intermediate layer known as a "hyperzone". 
The APU contains hyperzones which contains zones. 
The hyperzones are groupings used for configuration purposes. 
A PlatformStatusReport will be sent for the APU containing a PlatformStatusReport for each hyperzone. 
Within each hyperzone, a DeviceStatusReport will be sent for each zone within that hyperzone.
500 시리즈 APU는 유사하지만 "하이퍼 존"이라는 중간 계층을 포함합니다.
APU에는 영역이 포함 된 하이퍼 존이 포함되어 있습니다.
하이퍼 존은 구성 목적으로 사용되는 그룹입니다.
각 하이퍼 존에 대한 PlatformStatusReport를 포함하는 APU에 대해 PlatformStatusReport가 전송됩니다.
각 하이퍼 존 내에서 해당 하이퍼 존 내의 각 영역에 대해 DeviceStatusReport가 전송됩니다



WARNING: The Status values within the PlatformStatusReport are notcomplete. 
In particular, when an APU is in a tamper condition, the APU's Status within the PlatformStatusReport will not indicate this.
경고 : PlatformStatusReport 내의 상태 값이 완전하지 않습니다.
특히 APU가 변조 상태 인 경우 PlatformStatusReport 내의 APU 상태는이를 나타내지 않습니다.

Also, when a zone is in a sensing fault condition, the Status value for the zone's DeviceStatusReport inside the PlatformStatusReport does not look the same as the status in a normal DeviceStatusReport. 
또한 영역이 감지 오류 상태에있는 경우 PlatformStatusReport 내 영역의 DeviceStatusReport에 대한 상태 값은 일반 DeviceStatusReport의 상태와 동일하지 않습니다.

Instead, it looks like this:
    <Status>
        <DeviceState>Fail</DeviceState>
        <CommunicationState>Fail</CommunicationState>
        <UpdateTime Zone="GMT">2003-07-19T11:43:03.000</UpdateTime>
    </Status>


After the "handshake" sequence is completed, a DeviceDetectionReport will be sent indicating any tamper and sensing fault conditions.
"핸드 셰이크"시퀀스가 완료되면 변조 및 감지 오류 상태를 나타내는 DeviceDetectionReport 가 전송됩니다.

A note about device names:

Full device names follow the hierarchical structure and use a period ('.') as a separator. 
Generally speaking, monitoring equipment should not need to parse the device name, just match the name up to previously identified names.
전체 장치 이름은 계층 구조를 따르고 마침표 ( '.')를 구분 기호로 사용합니다.
일반적으로 모니터링 장비는 장치 이름을 구문 분석 할 필요가 없으며 이름을 이전에 식별 된 이름과 일치시키기 만하면됩니다.

The full name of a 300 series zone is "apu.zone", where "apu" is the name of the APU and "zone" is the partial name of the zone. 
The full name of a 500 series zone is "apu.hyperzone.zone", where "hyperzone" is the name of the hyperzone.
300 시리즈 영역의 전체 이름은 "apu.zone"입니다. 여기서 "apu"는 APU의 이름이고 "zone"은 영역의 부분 이름입니다.
500 시리즈 영역의 전체 이름은 "apu.hyperzone.zone"이며 여기서 "hyperzone"은 하이퍼 존의 이름입니다.

It is important to recognize that the component parts of names can, in general, be edited by a user using the APU configuration software, so they should not be relied upon to have any particular form. 
However, if you are confused about a name that you are seeing, this may help you.
APU 구성 소프트웨어를 사용하는 사용자이므로 특정 형태를 갖도록 의존해서는 안됩니다.
그러나 보고있는 이름이 혼동되는 경우 도움이 될 수 있습니다.

By default, a 300 series APU has a name equal "E" plus the serial number.  
By default, the partial name of the first zone is "CHA" and the second zone is "CHB".
Some example 300 series names: "E100213" (an APU), "E100213.CHA" (a zone), "FOO" (an APU), and "FOO.BAR", (a zone).
By default, the APU has a name equal to "model-serial", where "model" is the model name and "serial" is the serial number. 
기본적으로 300 시리즈 APU의 이름은 "E"에 일련 번호를 더한 이름입니다.
기본적으로 첫 번째 영역의 부분 이름은 "CHA"이고 두 번째 영역은 "CHB"입니다.
300 시리즈 이름의 예 : "E100213"(APU), "E100213.CHA"(영역), "FOO"(APU) 및 "FOO.BAR", (영역)
기본적으로 APU의 이름은 "model-serial"과 동일합니다. 여기서 "model"은 모델 이름이고 "serial"은 일련 번호입니다.

Hyperzones have partial names "HZONE-#", where "#" is the number of the hyperzone. Users cannot change hyperzone names. 
By default, partial zone names have the form "ZONE-###", where "###" is the 3-digit number of the zone. 
하이퍼 존은 부분 이름 "HZONE- #"을 가지며, 여기서 "#"은 하이퍼 존의 번호입니다. 사용자는 하이퍼 존 이름을 변경할 수 없습니다.
기본적으로 부분 영역 이름의 형식은 "ZONE-###"이며, 여기서 "###"은 영역의 3 자리 숫자입니다.

The hyperzone partial names cannot be changed, although the arrangement of which hyperzones contain which zones can also be set using the APU configuration software. 
By default, all zones are in the first hyperzone.
하이퍼 존 부분 이름은 변경할 수 없지만, 하이퍼 존에 포함되는 배열은 APU 구성 소프트웨어를 사용하여 설정할 수도 있습니다.
기본적으로 모든 영역은 첫 번째 하이퍼 영역에 있습니다.

 
Some example 500 series names: 
"FD508-100213" (an APU),
"FD508-100213.HZONE-3" (a hyperzone),
"FD508-100213.HZONE-3.ZONE-012" (a zone), 
"FOO" (an APU),
"FOO.HZONE-1", (a hyperzone), 
"FOO.HZONE-1.BAZ" (a zone).



Please refer to AN-SM-009 for a description of the "handshake" when communicating with an APU. 
This is essential to understanding communication.
APU와 통신 할 때 "핸드 셰이크"에 대한 설명은 AN-SM-009를 참조하십시오.
이것은 의사 소통을 이해하는 데 필수적입니다.

Example 300 series PlatformStatusReport message:
    <?xml version="1.0" encoding="UTF-8"?>
    <PlatformStatusReport>
        <PlatformIdentification>
            <DeviceName>E102147</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>FD34x APU</DeviceType>
        </PlatformIdentification>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>E102147.CHA</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>FD34x Channel</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2014-05-14T12:05:02.000</UpdateTime>
            </Status>
        </DeviceStatusReport>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>E102147.CHB</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>FD34x Channel</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2014-05-14T12:05:02.000</UpdateTime>
            </Status>
        </DeviceStatusReport>
    </PlatformStatusReport>


Example 500 series PlatformStatusReport message:
    <?xml version="1.0" encoding="UTF-8"?>
    <PlatformStatusReport>
        <PlatformIdentification>
        <DeviceName>FD508-100913</DeviceName>
        <DeviceCategory>Sensor</DeviceCategory>
        <DeviceType>SPIDR APU</DeviceType>
        </PlatformIdentification>
        <PlatformStatusReport>
        <PlatformIdentification>
            <DeviceName>FD508-100913.HZONE-1</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Hyperzone</DeviceType>
        </PlatformIdentification>
        <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.856</UpdateTime>
        </Status>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-1.ZONE-001</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.857</UpdateTime>
            </Status>
        </DeviceStatusReport>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-1.ZONE-003</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.858</UpdateTime>
            </Status>
        </DeviceStatusReport>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-1.ZONE-005</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.859</UpdateTime>
            </Status>
        </DeviceStatusReport>
        </PlatformStatusReport>
        <PlatformStatusReport>
        <PlatformIdentification>
            <DeviceName>FD508-100913.HZONE-2</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Hyperzone</DeviceType>
        </PlatformIdentification>
        <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.860</UpdateTime>
        </Status>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-2.ZONE-002</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.861</UpdateTime>
            </Status>
        </DeviceStatusReport>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-2.ZONE-004</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.861</UpdateTime>
            </Status>
        </DeviceStatusReport>
        <DeviceStatusReport>
            <DeviceIdentification>
            <DeviceName>FD508-100913.HZONE-2.ZONE-006</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>SPIDR Zone</DeviceType>
            </DeviceIdentification>
            <Status>
            <DeviceState>Secure</DeviceState>
            <CommunicationState>OK</CommunicationState>
            <UpdateTime Zone="GMT">2070-01-03T08:12:26.862</UpdateTime>
            </Status>
        </DeviceStatusReport>
        </PlatformStatusReport>
    </PlatformStatusReport>

-------------------------------------

Example message from APU when an intrusion occurs on a zone:
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceDetectionReport>
        <DeviceDetectionRecord>
        <DeviceIdentification>
            <DeviceName>APUNAME.CHB</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>FD34x Channel</DeviceType>
        </DeviceIdentification>
        <Detection>
            <ID>SZ0014</ID>
            <DetectionEvent>Intrusion</DetectionEvent>
            <UpdateTime Zone="GMT">2016-03-10T15:42:24.000</UpdateTime>
        </Detection>
        </DeviceDetectionRecord>
    </DeviceDetectionReport>


Example message from APU when a sensing fault occurs on a zone:
    <?xml version="1.0" encoding="UTF-8"?>
    <DeviceDetectionReport>
        <DeviceDetectionRecord>
        <DeviceIdentification>
            <DeviceName>APUNAME.CHB</DeviceName>
            <DeviceCategory>Sensor</DeviceCategory>
            <DeviceType>FD34x Channel</DeviceType>
        </DeviceIdentification>
        <Detection>
            <ID>SZ0016</ID>
            <DetectionEvent>Fault</DetectionEvent>
            <UpdateTime Zone="GMT">2016-03-10T15:42:42.000</UpdateTime>
        </Detection>
        </DeviceDetectionRecord>
    </DeviceDetectionReport>


NOTE: These detection reports occur at the time of occurrence. 
They do not reflect ongoing state. For intrusion occurrence, this is expected, since "intrusion" is an instantaneous activity. 
However, sensing faults can begin and end. 
Observe DeviceStatusReport messages to track ongoing device state for sensing faults.
참고 : 이러한 탐지 보고서는 발생 시점에 발생합니다.
진행중인 상태를 반영하지 않습니다. 침입 발생의 경우 "침입"이 즉각적인 활동이기 때문에 예상됩니다.
그러나 감지 오류는 시작되고 끝날 수 있습니다.
DeviceStatusReport 메시지를 관찰하여 오류 감지를 위해 진행중인 장치 상태를 추적합니다.


