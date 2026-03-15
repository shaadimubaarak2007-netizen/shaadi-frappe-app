import { ref } from 'vue'
import { Dialog } from 'frappe-ui'

const showDialog = ref(false)
const dialogConfig = ref({})

export function useConfirmDialog() {
  const confirm = (config) => {
    return new Promise((resolve) => {
      dialogConfig.value = {
        title: config.title || 'Confirm Action',
        message: config.message || 'Are you sure you want to proceed?',
        confirmText: config.confirmText || 'Confirm',
        cancelText: config.cancelText || 'Cancel',
        variant: config.variant || 'solid',
        theme: config.theme || 'blue',
        onConfirm: () => {
          showDialog.value = false
          resolve(true)
        },
        onCancel: () => {
          showDialog.value = false
          resolve(false)
        }
      }
      showDialog.value = true
    })
  }

  const success = (config) => {
    return new Promise((resolve) => {
      dialogConfig.value = {
        title: config.title || 'Success',
        message: config.message || 'Action completed successfully!',
        confirmText: config.confirmText || 'OK',
        variant: 'solid',
        theme: 'green',
        showCancel: false,
        onConfirm: () => {
          showDialog.value = false
          resolve(true)
        }
      }
      showDialog.value = true
    })
  }

  const error = (config) => {
    return new Promise((resolve) => {
      dialogConfig.value = {
        title: config.title || 'Error',
        message: config.message || 'An error occurred. Please try again.',
        confirmText: config.confirmText || 'OK',
        variant: 'solid',
        theme: 'red',
        showCancel: false,
        onConfirm: () => {
          showDialog.value = false
          resolve(true)
        }
      }
      showDialog.value = true
    })
  }

  return {
    showDialog,
    dialogConfig,
    confirm,
    success,
    error
  }
}
