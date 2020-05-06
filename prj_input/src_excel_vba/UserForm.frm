VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} UserForm 
   Caption         =   "入力フォーム"
   ClientHeight    =   5480
   ClientLeft      =   110
   ClientTop       =   450
   ClientWidth     =   7020
   OleObjectBlob   =   "UserForm.frx":0000
   StartUpPosition =   1  'オーナー フォームの中央
End
Attribute VB_Name = "UserForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public patientSheet As String
Public sh1 As Worksheet


Private Sub CommandButton2_Click()
    Dim range1, findRange, findObj, multiFind As Range

    
    Dim v As Integer
    Dim msg As String

    
    Set range1 = Range("A3:A20")
    v = TextBox3.Value
    
    Set findObj = range1.Find(v, Lookat:=xlWhole)
    
    If findObj Is Nothing Then
        MsgBox "'" & v & "'はありませんでした。"
        Exit Sub
    Else
        msg = "'" & v & "'は" & findObj.Row & "行目にあります。" & vbCrLf
    End If
    
    Set multiFind = findObj
    Set multiFind = range1.FindNext(multiFind)
    If multiFind.Address = findObj.Address Then
        MsgBox msg
        TextBox1.Value = v
        Exit Sub
    Else
        msg = "複数個見つかりました" & vbCrLf & msg
        msg = msg & "'" & v & "'は" & multiFind.Row & "行目にあります。" & vbCrLf
        Do While Not findObj Is Nothing
            Set multiFind = range1.FindNext(multiFind)
            
            If multiFind.Address = findObj.Address Then
                Exit Do
            End If
            msg = msg & "'" & v & "'は" & multiFind.Row & "行目にあります。" & vbCrLf
        Loop
    End If
    MsgBox msg
    TextBox1.Value = ""
    
End Sub


Private Sub TextBox3_Change()

End Sub

Private Sub UserForm_initialize()
    ComboBox1.Clear
    ComboBox1.AddItem "A"
    ComboBox1.AddItem "B"
    ComboBox1.AddItem "C"
    
    patientSheet = "患者情報入力シート"
    
    Set sh1 = Worksheets(patientSheet)
End Sub


Private Sub ComboBox1_Change()
    Dim c1 As Range
    Set c1 = sh1.Range("B4")
    Select Case ComboBox1.Value
        Case "A"
            c1.Value = "A1"
        Case "B"
            c1.Value = "B2"
        Case "C"
            c1.Value = "C3"
    End Select
End Sub

Private Sub CommandButton1_Click()
    sh1.Range("B3").Value = TextBox1.Value
End Sub

Private Sub Label1_Click()

End Sub

Private Sub TextBox1_Change()
    
End Sub

Private Sub TextBox2_Change()

End Sub

Private Sub UserForm_Click()

End Sub
