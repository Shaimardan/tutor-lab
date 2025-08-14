/* eslint-disable no-console */
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, combineLatest, filter, startWith } from 'rxjs';
import { MachineHistoryItem } from '../../openapi/models/machine-history-item';

@Injectable({
  providedIn: 'root',
})
export class WSService {
  presetsListUpdated$ = new BehaviorSubject<string>('');

  presetUpdated$ = new BehaviorSubject<string>('');

  assetStatusUpdate$ = new BehaviorSubject<string>('');

  wizardFileProgress$ = new BehaviorSubject<string>('');

  portalSrtatusUpdate$ = new BehaviorSubject<string>('');

  machineHistoryUpdate$ = new BehaviorSubject<MachineHistoryItem | undefined>(undefined);

  constructor() {
    this.connect();
  }

  getPresetUpdatedByIdPipe(id$: Observable<string>) {
    return combineLatest([id$, this.presetUpdated$]).pipe(
      startWith([null, null]),
      filter(([id, updatedId]) => id === updatedId),
    );
  }

  connect() {
    const ws = new WebSocket(`ws://${window.location.host}/api/ws`);
    ws.onmessage = (event: { data: string }) => {
      if (event.data.startsWith('WS')) {
        return;
      }
      try {
        const data = JSON.parse(event.data);
        switch (data.event) {
          case 'PRESET_LIST_UPDATED':
            this.presetsListUpdated$.next('');
            break;
          case 'PRESET_UPDATED':
            this.presetUpdated$.next(data.id.toString());
            break;
          case 'ASSET_DOWNLOAD_COMPLETE':
            this.assetStatusUpdate$.next('');
            break;

          case 'FILE_STATUS_UPDATE':
            this.wizardFileProgress$.next('');
            break;

          case 'PORTAL_STATUS_UPDATE':
            this.portalSrtatusUpdate$.next('');
            break;

          case 'MACHINE_HISTORY_UPDATE':
            this.machineHistoryUpdate$.next({
              id: data.id,
              operation: data.operation,
              date: data.date,
            } as MachineHistoryItem);
            break;

          default:
            console.error('Unknown event', data.event);
        }
      } catch (e) {
        console.error('Error', e);
      }
    };

    ws.onopen = () => {
      console.info('connected');
      ws.send('WS ping');
    };

    ws.onclose = () => {
      console.info('disconnected');

      setTimeout(() => {
        console.info('reconnecting');
        this.connect();
      }, 1000);
    };
  }
}
