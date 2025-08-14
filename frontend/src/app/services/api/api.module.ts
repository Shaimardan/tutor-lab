import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PingService } from './ping/ping.service';
import { UserService } from './user.service';
import { AvailabilitiesService } from './availabilities.service';

@NgModule({
  declarations: [],
  imports: [CommonModule],
  providers: [PingService, UserService, AvailabilitiesService],
})
export class ApiModule {}
