export class User {
    id!: number;
    phone!: string;
    role!: string;
    active!: boolean;
    password?: string;
  
    constructor(data: Partial<User>) {
      Object.assign(this, data);
    }
  }