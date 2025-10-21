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
	float prev_speed = 0;
	float speed = 0;
	float prev_acceleration = 0;
	float acceleration = 0;
	float jerk = 0;
	bool isFinished = false;
	int _curCP = 0;
	int _curLap = 0;
	while (true) {
		CSceneVehicleVisState@ vehicle = VehicleState::ViewingPlayerState();

		auto sock_serv = Net::Socket();
		if (!sock_serv.Listen("127.0.0.1", 9000)) {
			print("Could not initiate server socket.");
			return;
		}
		print(Time::Now + ": Waiting for incoming connection...");

		while(!sock_serv.Available()){
			yield();
		}
		print("Socket can read");
		auto sock = sock_serv.Accept();

		print(Time::Now + ": Accepted incomming connection.");

		while (!sock.CanWrite()) {
			yield();
		}
		print("Socket can write");
		print(Time::Now + ": Connected!");

		// OpenPlanet can store bytes in a MemoryBuffer:
		MemoryBuffer@ buf = MemoryBuffer(0);

		bool cc = true;
		while(cc)
		{
			CTrackMania@ app = cast<CTrackMania>(GetApp());
			if(app is null)
			{
				yield();
				continue;
			}
			CSmArenaClient@ playground = cast<CSmArenaClient>(app.CurrentPlayground);
			if(playground is null)
			{
				yield();
				continue;
			}
			CSmArena@ arena = cast<CSmArena>(playground.Arena);
			if(arena is null)
			{
				yield();
				continue;
			}
			if(arena.Players.Length <= 0)
			{
				yield();
				continue;
			}

			auto player = arena.Players[0];
			if(player is null)
			{
				yield();
				continue;
			}
			if(vehicle is null)
			{
				yield();
				continue;
			}
			auto race_state = playground.GameTerminals[0].UISequence_Current;
			speed = vehicle.FrontSpeed;
      		acceleration = speed - prev_speed;
			jerk = acceleration - prev_acceleration;
      		prev_speed = speed;
			prev_acceleration = acceleration;

            if(race_state == SGamePlaygroundUIConfig::EUISequence::Finish || race_state == SGamePlaygroundUIConfig::EUISequence::EndRound)
			{
				isFinished = true;
			}
			else
			{
				isFinished = false;
			}

			buf.Seek(0, 0);
			// Sending data
            append_float(buf, vehicle.FrontSpeed); // speed
			append_float(buf, acceleration); // acceleration
			append_float(buf, jerk); // jerk
			append_bool(buf, isFinished); // course status

			buf.Seek(0, 0);
	    	cc = send_memory_buffer(sock, buf);

			yield(); 
		}
		sock.Close();
		sock_serv.Close();
	}
}