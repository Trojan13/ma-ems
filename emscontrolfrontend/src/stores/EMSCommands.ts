import { defineStore } from 'pinia'

export const useEMSCommandsStore = defineStore('emscommands', {
  state: () => ({
    commands_history: [] as string[]
  }),
  getters: {},

  actions: {
    sendCommand(command: string) {
      this.commands_history.push(command)
    }
  }
})
