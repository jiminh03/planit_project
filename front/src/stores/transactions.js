// stores/transactions.js
import { defineStore } from 'pinia'
import axios from 'axios'

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

export const useTransactionStore = defineStore('transaction', {
  state: () => ({
    transactions: []
  }),
  actions: {
    addTransaction(payload) {
      this.transactions.push(payload)
    },
    updateTransaction: async function(index, updatedData) {
      try {
        const target = this.transactions[index]
        if (!target || !target.id || !updatedData) {
          console.warn('업데이트 대상이 유효하지 않음:', target)
          return
        }

        const endpoint = target.amount > 0
          ? `http://localhost:8000/api/home/incomes/${target.id}/`
          : `http://localhost:8000/api/home/expenses/${target.id}/`

        const res = await axios.put(endpoint, updatedData, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        })

        this.transactions[index] = res.data
        console.log('✅ 거래 업데이트 완료:', res.data)
      } catch (err) {
        console.error('❌ 거래 업데이트 실패:', err)
      }
    },

    deleteTransaction: async function(index) {
      try {
        const target = this.transactions[index]
        if (!target || !target.id) {
          console.warn('삭제 대상이 유효하지 않음:', target)
          return
        }

        const endpoint = target.amount > 0
          ? `http://localhost:8000/api/home/incomes/${target.id}/`
          : `http://localhost:8000/api/home/expenses/${target.id}/`

        await axios.delete(endpoint, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        })

        this.transactions.splice(index, 1)
        console.log('🗑️ 거래 삭제 완료:', target)
      } catch (err) {
        console.error('❌ 거래 삭제 실패:', err)
      }
    },


    // API 연동 actions
    async fetchTransactions(year, month) {
      if (!year || !month) {
        console.warn('❌ fetchTransactions called with undefined year or month:', { year, month })
        return
      }
      try {
        console.log(`[FETCH 요청] /incomes/?year=${year}&month=${month}`)
        const incomeRes = await axios.get(`http://localhost:8000/api/home/incomes/?year=${year}&month=${month}`, { withCredentials: true })
        console.log('[DEBUG] 수입 응답:', incomeRes.data)

        console.log(`[FETCH 요청] /expenses/?year=${year}&month=${month}`)
        const expenseRes = await axios.get(`http://localhost:8000/api/home/expenses/?year=${year}&month=${month}`, { withCredentials: true })
        console.log('[DEBUG] 지출 응답:', expenseRes.data)

        const combined = [...incomeRes.data, ...expenseRes.data].map(t => {
          return {
            ...t,
            date: typeof t.date === 'string' ? t.date : new Date(t.date).toISOString().split('T')[0]
          }
        })

        this.transactions = combined
        console.log('✅ 모든 거래 날짜:', this.transactions.map(t => t.date))
      } catch (error) {
        console.error('거래내역 불러오기 실패:', error)
      }
    },

    async fetchAllTransactions() {
      try {
        console.log(`[FETCH 요청] /incomes/ (전체)`)
        const incomeRes = await axios.get(`http://localhost:8000/api/home/incomes/`, { withCredentials: true })
        console.log('[DEBUG] 전체 수입 응답:', incomeRes.data)
        if (!Array.isArray(incomeRes.data)) {
          console.warn('Unexpected income data format:', incomeRes.data)
        }

        console.log(`[FETCH 요청] /expenses/ (전체)`)
        const expenseRes = await axios.get(`http://localhost:8000/api/home/expenses/`, { withCredentials: true })
        console.log('[DEBUG] 전체 지출 응답:', expenseRes.data)
        if (!Array.isArray(expenseRes.data)) {
          console.warn('Unexpected expense data format:', expenseRes.data)
        }

        const combined = [...incomeRes.data, ...expenseRes.data].map(t => ({
          ...t,
          _parsedDate: new Date(t.date),
        }))
          .sort((a, b) => b._parsedDate - a._parsedDate)
          .map(({ _parsedDate, ...rest }) => ({
            ...rest,
            date: new Date(rest.date).toISOString().split('T')[0],
          }))

        this.transactions = combined
      } catch (error) {
        console.error('전체 거래내역 불러오기 실패:', error)
      }
    },

    async addIncome(data) {
      try {
        const res = await axios.post('http://localhost:8000/api/home/incomes/', data, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
        this.transactions.push(res.data)
      } catch (error) {
        console.error('수입 등록 실패:', error)
      }
    },

    async addExpense(data) {
      try {
        const res = await axios.post('http://localhost:8000/api/home/expenses/', data, {
          withCredentials: true,
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
        this.transactions = [...this.transactions, res.data]
      } catch (error) {
        console.error('지출 등록 실패:', error)
      }
    },
  },
  getters: {
    getByDate: (state) => (date) =>
      state.transactions
        .map((t, i) => ({ ...t, _index: i })) // 수정/삭제용 인덱스 포함
        .filter(t => new Date(t.date).toISOString().split('T')[0] === date)
  }
})



