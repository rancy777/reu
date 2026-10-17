(define-fun bswap8 ((value (_ BitVec 8))) (_ BitVec 8)
    value
)

(define-fun bswap16 ((value (_ BitVec 16))) (_ BitVec 16)
  (bvor
    (bvshl
      (bvand value (_ bv255 16))
      (_ bv8 16)
    )
    (bvand (bvlshr value (_ bv8 16)) (_ bv255 16))
  )
)

(define-fun bswap32 ((value (_ BitVec 32))) (_ BitVec 32)
  (bvor
    (bvshl
      (bvor
        (bvshl
          (bvor
            (bvshl
              (bvand value (_ bv255 32))
              (_ bv8 32)
            )
            (bvand (bvlshr value (_ bv8 32)) (_ bv255 32))
          )
          (_ bv8 32)
        )
        (bvand (bvlshr value (_ bv16 32)) (_ bv255 32))
      )
      (_ bv8 32)
    )
    (bvand (bvlshr value (_ bv24 32)) (_ bv255 32))
  )
)

(define-fun bswap64 ((value (_ BitVec 64))) (_ BitVec 64)
  (bvor
    (bvshl
      (bvor
        (bvshl
          (bvor
            (bvshl
              (bvor
                (bvshl
                  (bvor
                    (bvshl
                      (bvor
                        (bvshl
                          (bvor
                            (bvshl
                              (bvand value (_ bv255 64))
                              (_ bv8 64)
                            )
                            (bvand (bvlshr value (_ bv8 64)) (_ bv255 64))
                          )
                          (_ bv8 64)
                        )
                        (bvand (bvlshr value (_ bv16 64)) (_ bv255 64))
                      )
                      (_ bv8 64)
                    )
                    (bvand (bvlshr value (_ bv24 64)) (_ bv255 64))
                  )
                  (_ bv8 64)
                )
                (bvand (bvlshr value (_ bv32 64)) (_ bv255 64))
              )
              (_ bv8 64)
            )
            (bvand (bvlshr value (_ bv40 64)) (_ bv255 64))
          )
          (_ bv8 64)
        )
        (bvand (bvlshr value (_ bv48 64)) (_ bv255 64))
      )
      (_ bv8 64)
    )
    (bvand (bvlshr value (_ bv56 64)) (_ bv255 64))
  )
)

(declare-fun x () (_ BitVec 32))
(define-fun ref!9139 () (_ BitVec 32) (bvnot x)) ; Extended part - NOT operation
(define-fun ref!9142 () (_ BitVec 32) (bvnot x)) ; Extended part - NOT operation
(define-fun ref!9149 () (_ BitVec 32) (bvand ref!9139 ref!9142)) ; Extended part - AND operation
(define-fun ref!9188 () (_ BitVec 32) (bvnot ref!9149)) ; Extended part - NOT operation
(define-fun ref!9224 () (_ BitVec 32) (bvand ref!9188 (_ bv2654435769 32))) ; Extended part - AND operation
(define-fun ref!9826 () (_ BitVec 32) (bvnot x)) ; Extended part - NOT operation
(define-fun ref!9831 () (_ BitVec 32) (bvand ref!9826 (_ bv1640531526 32))) ; Extended part - AND operation
(define-fun ref!9900 () (_ BitVec 32) (bvor ref!9831 ref!9224)) ; Extended part - OR operation
(define-fun ref!9918 () (_ BitVec 32) (bvnot ref!9900)) ; Extended part - NOT operation
(define-fun ref!13079 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!9918 ref!9918)))) ; Extended part - MOV operation
(define-fun ref!13112 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!13079)) ; Extended part - IMUL operation
(define-fun ref!17303 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!13112)) ; Extended part - ADC operation
(define-fun ref!17741 () (_ BitVec 32) (bvnot ref!17303)) ; Extended part - NOT operation
(define-fun ref!19421 () (_ BitVec 32) (bvnot ref!17741)) ; Extended part - NOT operation
(define-fun ref!19439 () (_ BitVec 32) (bvnot ref!17741)) ; Extended part - NOT operation
(define-fun ref!19458 () (_ BitVec 32) (bvand ref!19421 ref!19439)) ; Extended part - AND operation
(define-fun ref!19474 () (_ BitVec 32) (bvnot ref!19458)) ; Extended part - NOT operation
(define-fun ref!19483 () (_ BitVec 32) (bvand ref!19474 (_ bv2671344829 32))) ; Extended part - AND operation
(define-fun ref!19940 () (_ BitVec 32) (bvor ref!17741 (_ bv2671344829 32))) ; Extended part - OR operation
(define-fun ref!19955 () (_ BitVec 32) (bvnot ref!19940)) ; Extended part - NOT operation
(define-fun ref!20289 () (_ BitVec 32) (bvor ref!19955 ref!19483)) ; Extended part - OR operation
(define-fun ref!20307 () (_ BitVec 32) (bvnot ref!20289)) ; Extended part - NOT operation
(define-fun ref!24080 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!20307 ref!20307)))) ; Extended part - MOV operation
(define-fun ref!24085 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!24080)) ; Extended part - IMUL operation
(define-fun ref!27686 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!24085)) ; Extended part - ADD operation
(define-fun ref!28140 () (_ BitVec 32) (bvnot ref!27686)) ; Extended part - NOT operation
(define-fun ref!29661 () (_ BitVec 32) (bvnot ref!28140)) ; Extended part - NOT operation
(define-fun ref!29668 () (_ BitVec 32) (bvor ref!29661 (_ bv2688253889 32))) ; Extended part - OR operation
(define-fun ref!30769 () (_ BitVec 32) (bvnot ref!28140)) ; Extended part - NOT operation
(define-fun ref!30816 () (_ BitVec 32) (bvand ref!30769 (_ bv2688253889 32))) ; Extended part - AND operation
(define-fun ref!30824 () (_ BitVec 32) (bvnot ref!30816)) ; Extended part - NOT operation
(define-fun ref!30856 () (_ BitVec 32) (bvnot ref!30824)) ; Extended part - NOT operation
(define-fun ref!30867 () (_ BitVec 32) (bvnot ref!29668)) ; Extended part - NOT operation
(define-fun ref!30876 () (_ BitVec 32) (bvor ref!30856 ref!30867)) ; Extended part - OR operation
(define-fun ref!34615 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!30876 ref!30876)))) ; Extended part - OR operation
(define-fun ref!34666 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!34615)) ; Extended part - IMUL operation
(define-fun ref!37567 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!34666)) ; Extended part - ADD operation
(define-fun ref!38059 () (_ BitVec 32) (bvnot ref!37567)) ; Extended part - NOT operation
(define-fun ref!39604 () (_ BitVec 32) (bvnot ref!38059)) ; Extended part - NOT operation
(define-fun ref!39611 () (_ BitVec 32) (bvor ref!39604 (_ bv2705162949 32))) ; Extended part - OR operation
(define-fun ref!40712 () (_ BitVec 32) (bvnot ref!38059)) ; Extended part - NOT operation
(define-fun ref!40759 () (_ BitVec 32) (bvand ref!40712 (_ bv2705162949 32))) ; Extended part - AND operation
(define-fun ref!40767 () (_ BitVec 32) (bvnot ref!40759)) ; Extended part - NOT operation
(define-fun ref!40798 () (_ BitVec 32) (bvand ref!40767 ref!39611)) ; Extended part - AND operation
(define-fun ref!40819 () (_ BitVec 32) (bvnot ref!40798)) ; Extended part - NOT operation
(define-fun ref!44274 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!40819 ref!40819)))) ; Extended part - OR operation
(define-fun ref!44325 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!44274)) ; Extended part - IMUL operation
(define-fun ref!47342 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!44325)) ; Extended part - ADC operation
(define-fun ref!47498 () (_ BitVec 32) (bvnot ref!47342)) ; Extended part - NOT operation
(define-fun ref!48829 () (_ BitVec 32) (bvnot ref!47498)) ; Extended part - NOT operation
(define-fun ref!48836 () (_ BitVec 32) (bvor ref!48829 (_ bv2722072009 32))) ; Extended part - OR operation
(define-fun ref!49704 () (_ BitVec 32) (bvnot ref!47498)) ; Extended part - NOT operation
(define-fun ref!49943 () (_ BitVec 32) (bvand ref!49704 (_ bv2722072009 32))) ; Extended part - AND operation
(define-fun ref!49962 () (_ BitVec 32) (bvnot ref!49943)) ; Extended part - NOT operation
(define-fun ref!50047 () (_ BitVec 32) (bvand ref!49962 ref!48836)) ; Extended part - AND operation
(define-fun ref!50068 () (_ BitVec 32) (bvnot ref!50047)) ; Extended part - NOT operation
(define-fun ref!53542 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!50068 ref!50068)))) ; Extended part - OR operation
(define-fun ref!53593 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!53542)) ; Extended part - IMUL operation
(define-fun ref!56832 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!53593)) ; Extended part - ADC operation
(define-fun ref!56988 () (_ BitVec 32) (bvnot ref!56832)) ; Extended part - NOT operation
(define-fun ref!58618 () (_ BitVec 32) (bvnot ref!56988)) ; Extended part - NOT operation
(define-fun ref!58636 () (_ BitVec 32) (bvnot ref!56988)) ; Extended part - NOT operation
(define-fun ref!58655 () (_ BitVec 32) (bvand ref!58618 ref!58636)) ; Extended part - AND operation
(define-fun ref!58671 () (_ BitVec 32) (bvnot ref!58655)) ; Extended part - NOT operation
(define-fun ref!58680 () (_ BitVec 32) (bvand ref!58671 (_ bv2738981069 32))) ; Extended part - AND operation
(define-fun ref!59137 () (_ BitVec 32) (bvor ref!56988 (_ bv2738981069 32))) ; Extended part - OR operation
(define-fun ref!59152 () (_ BitVec 32) (bvnot ref!59137)) ; Extended part - NOT operation
(define-fun ref!59486 () (_ BitVec 32) (bvor ref!59152 ref!58680)) ; Extended part - OR operation
(define-fun ref!59504 () (_ BitVec 32) (bvnot ref!59486)) ; Extended part - NOT operation
(define-fun ref!62918 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!59504 ref!59504)))) ; Extended part - OR operation
(define-fun ref!62969 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!62918)) ; Extended part - IMUL operation
(define-fun ref!64989 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!62969)) ; Extended part - ADD operation
(define-fun ref!65327 () (_ BitVec 32) (bvnot ref!64989)) ; Extended part - NOT operation
(define-fun ref!66780 () (_ BitVec 32) (bvnot ref!65327)) ; Extended part - NOT operation
(define-fun ref!66819 () (_ BitVec 32) (bvor ref!66780 (_ bv2755890129 32))) ; Extended part - OR operation
(define-fun ref!67823 () (_ BitVec 32) (bvnot ref!65327)) ; Extended part - NOT operation
(define-fun ref!68062 () (_ BitVec 32) (bvand ref!67823 (_ bv2755890129 32))) ; Extended part - AND operation
(define-fun ref!68081 () (_ BitVec 32) (bvnot ref!68062)) ; Extended part - NOT operation
(define-fun ref!68166 () (_ BitVec 32) (bvand ref!68081 ref!66819)) ; Extended part - AND operation
(define-fun ref!68187 () (_ BitVec 32) (bvnot ref!68166)) ; Extended part - NOT operation
(define-fun ref!71509 () (_ BitVec 32) ((_ extract 31 0) ((_ rotate_right 27) (concat ref!68187 ref!68187)))) ; Extended part - MOV operation
(define-fun ref!71542 () (_ BitVec 32) (bvmul (_ bv2048144789 32) ref!71509)) ; Extended part - IMUL operation
(define-fun ref!75124 () (_ BitVec 32) (bvadd (_ bv1028477386 32) ref!71542)) ; Extended part - ADD operation
(define-fun ref!75567 () (_ BitVec 32) (bvnot ref!75124)) ; Extended part - NOT operation
(define-fun ref!75585 () (_ BitVec 32) (bvnot ref!75124)) ; Extended part - NOT operation
(define-fun ref!75599 () (_ BitVec 32) (bvand ref!75567 ref!75585)) ; Extended part - AND operation
(define-fun ref!76337 () (_ BitVec 8) ((_ extract 31 24) ref!75599)) ; Byte reference - MOV operation
(define-fun ref!76338 () (_ BitVec 8) ((_ extract 23 16) ref!75599)) ; Byte reference - MOV operation
(define-fun ref!76339 () (_ BitVec 8) ((_ extract 15 8) ref!75599)) ; Byte reference - MOV operation
(define-fun ref!76340 () (_ BitVec 8) ((_ extract 7 0) ref!75599)) ; Byte reference - MOV operation
(define-fun ref!76709 () (_ BitVec 8) (_ bv0 8)) ; Byte reference - MOV operation
(define-fun ref!76710 () (_ BitVec 8) (_ bv0 8)) ; Byte reference - MOV operation
(define-fun ref!76711 () (_ BitVec 8) (_ bv0 8)) ; Byte reference - MOV operation
(define-fun ref!76712 () (_ BitVec 8) (_ bv0 8)) ; Byte reference - MOV operation
(define-fun ref!79100 () (_ BitVec 8) ref!76709) ; Byte reference - MOV operation
(define-fun ref!79101 () (_ BitVec 8) ref!76710) ; Byte reference - MOV operation
(define-fun ref!79102 () (_ BitVec 8) ref!76711) ; Byte reference - MOV operation
(define-fun ref!79103 () (_ BitVec 8) ref!76712) ; Byte reference - MOV operation
(define-fun ref!79104 () (_ BitVec 8) ref!76337) ; Byte reference - MOV operation
(define-fun ref!79105 () (_ BitVec 8) ref!76338) ; Byte reference - MOV operation
(define-fun ref!79106 () (_ BitVec 8) ref!76339) ; Byte reference - MOV operation
(define-fun ref!79107 () (_ BitVec 8) ref!76340) ; Byte reference - MOV operation
(define-fun ref!115442 () (_ BitVec 64) (concat ref!79100 ref!79101 ref!79102 ref!79103 ref!79104 ref!79105 ref!79106 ref!79107)) ; MOV operation
(define-fun ref!115520 () (_ BitVec 32) ((_ extract 31 0) ref!115442)) ; Extended part - MOV operation
(define-fun ref!115536 () (_ BitVec 32) ref!115520) ; recovered-return
