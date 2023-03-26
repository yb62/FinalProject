import { ReactNode } from 'react';

declare module '@blueprintjs/select' {
  export interface TooltipProps {
    children: ReactNode;
  }
}