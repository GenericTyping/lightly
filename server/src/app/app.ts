import fetch from 'cross-fetch';
import { initializeApp } from 'firebase/app';
import { firebaseConfig } from '../firebaseConfig';
import { getFirestore, doc, onSnapshot } from 'firebase/firestore';

type RgbValue = [number, number, number];

type RgbDoc = Record<string, RgbValue>;

const localServerConfig = {
  host: '192.168.68.135',
  port: 1234,
};

const lightsCollectionName = 'lights';
const lightsDocName = 'current';

export const runApp = async () => {
  const firebaseApp = initializeApp(firebaseConfig);
  const db = getFirestore(firebaseApp);

  const unsub = onSnapshot(
    doc(db, `${lightsCollectionName}/${lightsDocName}`),
    (doc) => {
      const data = doc.data() as RgbDoc;
      console.log('Data updated!', data);
      setLight(data);
    }
  );

  process.on('SIGINT', () => {
    console.log('Quitting...');
    unsub();
    process.exit(0);
  });
};

const setLight = async (rgb: RgbDoc) => {
  const res = await fetch(
    `http://${localServerConfig.host}:${localServerConfig.port}/set`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(rgb),
    }
  );
  if (!res.ok) {
    console.error('Failed to set light', {
      status: res.status,
      statusText: res.statusText,
    });
  }
};
