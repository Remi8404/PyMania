// Palamabron - GetData Plugin
bool send_memory_buffer(Net::Socket@ sock, MemoryBuffer@ buf)
{
	if (!sock.Write(buf))
	{
		print("INFO: Disconnected, could not send data.");
		return false;
	}
	return true;
}

void append_float(MemoryBuffer@ buf, float val)
{
	buf.Write(val);
}

void append_bool(MemoryBuffer@ buf, bool val)
{
	if (val)
	{
		buf.Write(1.0f);
	}
	else
	{
		buf.Write(0.0f);

	}
}

void append_int(MemoryBuffer@ buf, int32 val)
{
	buf.Write(float(val));
}

// Main function - send data through socket on port 9000 - get inputs through port 9001
void Main()
{
   while (true) {
      //const float SideSpeed = VehicleState::GetSideSpeed();
      print(Text::Format("%.2f", 12.565456));
      yield();
   }
}