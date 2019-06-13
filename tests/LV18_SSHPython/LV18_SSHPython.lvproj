<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="EV3_Python.vi" Type="VI" URL="/Z/Dan On My Mac/Documents/CEEO19/ProgrammingHub/tests/LV18_SSHPython/EV3_Python.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
			</Item>
			<Item Name="CleanReplyEV3.vi" Type="VI" URL="/Z/Dan On My Mac/Documents/CEEO19/ProgrammingHub/tests/LV18_SSHPython/_subs/VIs/CleanReplyEV3.vi"/>
			<Item Name="CleanText.vi" Type="VI" URL="/Z/Dan On My Mac/Documents/CEEO19/ProgrammingHub/tests/LV18_SSHPython/_subs/VIs/CleanText.vi"/>
			<Item Name="PingBrick.vi" Type="VI" URL="/Z/Dan On My Mac/Documents/CEEO19/ProgrammingHub/tests/LV18_SSHPython/_subs/VIs/PingBrick.vi"/>
			<Item Name="SSHBrick.vi" Type="VI" URL="/Z/Dan On My Mac/Documents/CEEO19/ProgrammingHub/tests/LV18_SSHPython/_subs/VIs/SSHBrick.vi"/>
			<Item Name="Typing.vi" Type="VI" URL="/Z/Dan On My Mac/Documents/CEEO19/ProgrammingHub/tests/LV18_SSHPython/_subs/VIs/Typing.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
